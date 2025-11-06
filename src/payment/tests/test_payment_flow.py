from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.conf import settings
from unittest.mock import patch, Mock
import hmac
import hashlib
import json
from shop.models import Category, Product, Order, OrderItem, Status
from payment.models import Payment
import pytest

User = get_user_model()


@pytest.mark.django_db
class TestPaymentFlow(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="customer@example.com", password="password"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Books1", description="Literature")
        self.product = Product.objects.create(
            name="The Great Gatsby", price="15.00", stock=5, category=self.category
        )

        # Create a pending order manually for testing the payment part
        self.order = Order.objects.create(
            user=self.user, total_price="30.00", status=Status.pending
        )
        OrderItem.objects.create(
            order=self.order, product=self.product, quantity=2, price="15.00"
        )

    @patch("payment.views.requests.get")
    @patch("payment.views.requests.post")
    def test_payment_initialization_and_webhook_confirmation(self, mock_post, mock_get):
        # --- Part 1: Initialize Payment ---

        # Configure the mock for a successful Chapa initialization
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {
                "status": "success",
                "data": {"checkout_url": "https://checkout.chapa.co/test"},
            },
        )

        init_data = {"order_id": self.order.id}
        response = self.client.post(
            "/api/v1/payments/initialize/", init_data, format="json"
        )
        self.assertEqual(response.status_code, 200)

        # Verify a pending Payment object was created
        payment = Payment.objects.get(order=self.order)
        self.assertEqual(payment.status, Status.pending)
        tx_ref = payment.transaction_ref

        # --- Part 2: Simulate and Test Webhook ---

        # Configure the mock for a successful Chapa verification
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"status": "success", "data": {"status": "success"}},
        )

        # Construct the webhook payload
        webhook_payload = {"tx_ref": tx_ref, "status": "success"}
        body = json.dumps(webhook_payload, separators=(",", ":")).encode("utf-8")

        # Generate the signature
        secret = settings.CHAPA_WEBHOOK_SECRET.encode("utf-8")
        computed_hash = hmac.new(secret, body, hashlib.sha256).hexdigest()

        headers = {
            "HTTP_CHAPA_SIGNATURE": computed_hash,
            "CONTENT_TYPE": "application/json",
        }

        response = self.client.post(
            "/api/v1/payments/webhook/", data=webhook_payload, format="json", **headers
        )
        # TODO: REMOVE DEBUG LINES
        print(str(response.data))
        self.assertEqual(response.status_code, 200)

        # 3. Assert Final State
        self.order.refresh_from_db()
        payment.refresh_from_db()
        self.assertEqual(self.order.status, Status.success)
        self.assertEqual(payment.status, Status.success)
