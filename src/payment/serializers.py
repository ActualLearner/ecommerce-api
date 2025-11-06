from rest_framework import serializers
from shop.models import Order, Status


class InitializePaymentSerializer(serializers.Serializer):
    """
    Validates the request to initialize a payment, ensuring the order
    is valid and ready for payment.
    """

    order_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        order_id = attrs.get("order_id")

        # The view will pass the request into the serializer's context.
        # This is the standard way to give serializers access to the request object.
        request = self.context.get("request")
        if not request or not hasattr(request, "user"):
            raise serializers.ValidationError("Serializer requires a request context.")

        # 1. Validate existence and ownership
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            raise serializers.ValidationError(
                "Order not found or you do not have permission to access it."
            )

        # 2. Business logic validation: Check if order is empty
        if order.order_items.count() < 1:
            raise serializers.ValidationError(
                "Cannot initiate payment for an empty order."
            )

        # 3. Business logic validation: Check if order status is 'pending'
        if order.status != Status.pending:
            raise serializers.ValidationError(
                f"This order cannot be paid for as its status is '{order.status}'."
            )

        # All validation passed.
        # Attach the fully-validated order object to the attributes dict.
        # This prevents the view from needing to query the database again.
        attrs["order"] = order
        return attrs
