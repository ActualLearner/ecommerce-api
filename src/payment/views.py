import hmac
import hashlib
import json
import requests
import uuid
import logging

logger = logging.getLogger(__name__)

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction

from shop.models import Order, Status
from .models import Payment
from .serializers import InitializePaymentSerializer


class InitializePaymentView(APIView):
    """
    Initializes a payment transaction with Chapa for a given order.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        serializer = InitializePaymentSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]

        # 3. Generate a unique transaction reference
        tx_ref = f"nexus-{order.id}-{uuid.uuid4().hex}"

        # 4. Prepare the payload for the Chapa API
        user = request.user

        payload = {
            "amount": str(order.total_price),  # Ensure amount is a string
            "currency": "ETB",
            "email": user.email,
            "first_name": user.first_name if user.first_name else "Customer",
            "last_name": user.last_name if user.last_name else "Name",
            "tx_ref": tx_ref,
            "callback_url": settings.BACKEND_CALLBACK_URL,
            "return_url": settings.FRONTEND_RETURN_URL,
            "customization": {
                "title": f"Shop Order {order.id}",  # Short, no special characters
                "description": f"Payment for order {order.id}",  # Simple, no special characters
            },
        }

        # 5. Make the request to Chapa's API
        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                "https://api.chapa.co/v1/transaction/initialize",
                json=payload,
                headers=headers,
                timeout=10,  # avoids hanging forever if Chapa is slow
            )
            response.raise_for_status()  # raises HTTPError if response status >= 400
            response_data = response.json()
        except requests.exceptions.HTTPError as e:

            chapa_error_details = e.response.text
            logger.error(
                "Chapa returned a client error for order %s. Details: %s",
                order.id,
                chapa_error_details,
            )
            # Return a 400 error to our frontend with Chapa's detailed message.
            return Response(
                {
                    "error": "The payment provider rejected the request.",
                    "details": chapa_error_details,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except requests.exceptions.Timeout:
            logger.error("Chapa request timed out for order %s", order.id)
            return Response(
                {"error": "Payment service timed out. Please try again later."},
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )

        except requests.exceptions.RequestException as e:
            logger.exception(
                "Failed to initialize payment for order %s: %s", order.id, str(e)
            )
            return Response(
                {"error": "Failed to connect to the payment provider."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # 6. Handle the response from Chapa
        if response_data.get("status") == "success":
            # Create a pending payment record in the database
            Payment.objects.create(
                order=order,
                transaction_ref=tx_ref,
                amount=order.total_price,
                status=Status.pending,
            )
            return Response(response_data["data"], status=status.HTTP_200_OK)
        else:
            # Otherwise, return failure
            logger.warning(
                "Payment initialization failed for order %s: %s",
                order.id,
                response_data,
            )
            return Response(
                {
                    "error": "Failed to initialize payment.",
                    "details": response_data.get("message", "Unknown error."),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class PaymentWebhookView(APIView):
    """
    Handles incoming webhooks from Chapa to update transaction status.
    This endpoint should be publicly accessible.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # 1. Verify the webhook signature for security
        signature = request.headers.get("chapa-signature")
        x_signature = request.headers.get("x-chapa-signature")
        body = request.body

        if not signature and not x_signature:
            return Response(
                {"error": "Missing signature header."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Recompute the hash and compare
        secret = settings.CHAPA_WEBHOOK_SECRET.encode("utf-8")
        x_computed_hash = hmac.new(secret, secret, hashlib.sha256).hexdigest()
        computed_hash = hmac.new(secret, body, hashlib.sha256).hexdigest()

        valid = False
        if signature and hmac.compare_digest(computed_hash, signature):
            valid = True
        elif x_signature and hmac.compare_digest(x_computed_hash, x_signature):
            valid = True

        if not valid:
            return Response(
                {"error": "Invalid signature."}, status=status.HTTP_403_FORBIDDEN
            )

        # 2. Parse the payload and get the transaction reference
        try:
            event_data = json.loads(body)
            tx_ref = event_data.get("tx_ref")
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON payload."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not tx_ref:
            return Response(
                {
                    "error": "Transaction reference (tx_ref) not found in webhook payload."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. Verify the transaction status with Chapa's API (Source of Truth)
        headers = {"Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"}
        try:
            verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
            response = requests.get(verify_url, headers=headers)
            response.raise_for_status()
            verification_data = response.json()
        except requests.exceptions.RequestException as e:
            # If verification fails, we should not proceed. Acknowledge the webhook to prevent retries
            # but log the error for manual investigation.
            # Log error: f"Failed to verify transaction {tx_ref} with Chapa: {e}"
            return Response(status=status.HTTP_200_OK)

        # 4. Update the database if verification is successful
        if (
            verification_data.get("status") == "success"
            and verification_data["data"]["status"] == "success"
        ):
            try:
                payment = Payment.objects.get(transaction_ref=tx_ref)

                # Use a database transaction to ensure atomicity
                with transaction.atomic():
                    # Update payment status to 'Completed'
                    payment.status = Status.success
                    payment.save()

                    # Update the related order's status (you may need to add a 'payment_status' field to your Order model)
                    order = payment.order

                    order.status = Status.success
                    order.save()

                    # here you can trigger other post-payment logic, like sending a confirmation email.

            except Payment.DoesNotExist:
                # The webhook is for a transaction not in our system. Log it and ignore.
                pass

        # 5. Acknowledge receipt of the webhook with a 200 OK
        return Response(status=status.HTTP_200_OK)
