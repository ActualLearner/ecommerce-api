from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, OrderItem, Order
from django.db import transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


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


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "category", "name", "description", "stock", "price"]


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


class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer to handle the creation of an order from a cart.
    This is a write-only serializer.
    """

    def save(self, **kwargs):
        cart = self.context["cart"]
        user = self.context["user"]

        if cart.cart_items.count() == 0:
            raise serializers.ValidationError(
                "Your cart is empty. Cannot create an order."
            )

        # Use a database transaction to ensure atomicity
        with transaction.atomic():
            # 1. Calculate total price from cart
            total_price = sum(
                item.product.price * item.quantity for item in cart.cart_items.all()
            )

            # 2. Create the Order
            order = Order.objects.create(
                user=user, total_price=total_price, status="success"
            )

            # 3. Create OrderItems from CartItems and check stock
            order_items_to_create = []
            for item in cart.cart_items.all():
                # Stock check
                if item.quantity > item.product.stock:
                    raise serializers.ValidationError(
                        f"Not enough stock for {item.product.name}. "
                        f"Available: {item.product.stock}, "
                        f"Requested: {item.quantity}"
                    )

                order_items_to_create.append(
                    OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,  # Record price at time of purchase
                    )
                )
                # 4. Decrease product stock
                item.product.stock -= item.quantity
                item.product.save()

            OrderItem.objects.bulk_create(order_items_to_create)

            # 5. Clear the cart
            cart.cart_items.all().delete()

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
