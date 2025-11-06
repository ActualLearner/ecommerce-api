from django.db import transaction
from django.db.models import F
from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, OrderItem, Order, Status
from django.db import transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    A 'write-only' serializer for creating and updating Product instances.
    It accepts a simple category ID for the foreign key relationship.
    This serializer is intended for use by admin users.
    """

    # By default, DRF treats ForeignKey fields as PrimaryKeyRelatedField,
    # so just including 'category' is enough to make it accept an ID.
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "category"]


class ProductListSerializer(serializers.ModelSerializer):
    # Use a simpler representation for the category in lists
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ["id", "name", "price", "stock", "category"]


class ProductDetailSerializer(serializers.ModelSerializer):
    # The full nested representation for detail views
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        # The full list of fields
        fields = ["id", "name", "description", "price", "stock", "category"]


class OrderItemSerializer(serializers.ModelSerializer):
    """Read-only serializer for items within an order."""

    product = ProductListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for viewing a user's orders."""

    order_items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ["id", "user", "created_at", "total_price", "status", "order_items"]


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Handles the creation of an order from a cart. Inherits from ModelSerializer
    to leverage its ability to return the created instance upon creation.
    """

    # We define the fields we want in the OUTPUT here. They are read-only
    # because they are not part of the input.
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        # The fields we want to be returned in the response
        fields = ["id", "user", "created_at", "total_price", "status", "order_items"]
        read_only_fields = fields  # Mark all as read-only for the output

    # We move the logic from `save()` to `create()`
    def create(self, validated_data):
        cart = self.context["cart"]
        user = self.context["user"]
        cart_items = cart.cart_items.all()

        if not cart_items:
            raise serializers.ValidationError(
                "Your cart is empty. Cannot create an order."
            )

        with transaction.atomic():
            # (Using the more robust version of this logic)
            product_ids = [item.product_id for item in cart_items]
            products = Product.objects.select_for_update().filter(id__in=product_ids)
            product_map = {p.id: p for p in products}

            total_price = sum(
                product_map[item.product_id].price * item.quantity
                for item in cart_items
            )

            # The ModelSerializer's .create() method is expected to create and return the instance
            order = Order.objects.create(
                user=user, total_price=total_price, status=Status.pending
            )

            order_items_to_create = []
            for item in cart_items:
                product = product_map[item.product_id]
                if item.quantity > product.stock:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name}."
                    )

                order_items_to_create.append(
                    OrderItem(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price=product.price,
                    )
                )
                product.stock = F("stock") - item.quantity
                product.save(update_fields=["stock"])

            OrderItem.objects.bulk_create(order_items_to_create)

            cart_items.delete()

            return order


class CartItemProductSerializer(serializers.ModelSerializer):
    """A lightweight serializer for Products within a CartItem."""

    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for adding/updating items in a cart."""

    product = CartItemProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity"]
        read_only_fields = ["id"]

    def validate(self, data):
        """
        Validates against available product stock before creating or updating.
        """
        quantity_requested = data["quantity"]
        product = data["product"]

        # Check if this is an update (self.instance exists) or a create
        if self.instance:
            # This is a PATCH request (update).
            # The validation is simple: the new quantity cannot exceed the total stock.
            if quantity_requested > product.stock:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}. "
                    f"Available: {product.stock}, Requested: {quantity_requested}"
                )
        else:
            # This is a POST request (create).
            # We need to check if the item is already in the cart.
            current_quantity_in_cart = 0
            try:
                cart_item = CartItem.objects.get(
                    cart=self.context["cart"], product=product
                )
                current_quantity_in_cart = cart_item.quantity
            except CartItem.DoesNotExist:
                pass  # Item is not in the cart yet.

            total_requested_quantity = current_quantity_in_cart + quantity_requested
            if total_requested_quantity > product.stock:
                raise serializers.ValidationError(
                    f"Not enough stock for {product.name}. "
                    f"Available: {product.stock}, Requested: {total_requested_quantity}"
                )

        return data

    def create(self, validated_data):
        # Get the user's cart from the context passed by the view
        cart = self.context["cart"]
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")

        # Use get_or_create to find or create a cart item
        # This prevents the IntegrityError
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        # If the item was not created, it means it already existed.
        # In this case, we update its quantity.
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the user's shopping cart."""

    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "cart_items", "total_price"]
        read_only_fields = ["id", "cart_items", "total_price"]

    def get_total_price(self, cart: Cart):
        return sum(item.product.price * item.quantity for item in cart.cart_items.all())
