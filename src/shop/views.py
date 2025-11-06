from django.shortcuts import render
from rest_framework import viewsets, filters, status, generics
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

# Import the new serializers and models needed for the cart
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductWriteSerializer,
    CategorySerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    CreateOrderSerializer,
)
from .models import Product, Category, Order, Cart, CartItem
from .filters import ProductFilter

# Create your views here.


@extend_schema_view(
    list=extend_schema(
        description="Get a paginated list of all products. Can be filtered by category slug."
    ),
    retrieve=extend_schema(description="Get details of a single product by it's ID."),
    create=extend_schema(description="[Admin Only] Create a new product."),
    update=extend_schema(description="[Admin Only] Fully update a product's details."),
    partial_update=extend_schema(
        description="[Admin Only] Partially update a product's details."
    ),
    destroy=extend_schema(
        description="[Admin Only] Delete a product from the catalog."
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related("category").order_by("created_at")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return ProductWriteSerializer

        return ProductDetailSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - Staff/Admins can do anything.
        - Authenticated users can read.
        - Unauthenticated users can read.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            # For write actions, only allow admin users
            self.permission_classes = [IsAdminUser]
        else:
            # For read actions (list, retrieve), anyone is allowed
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()


@extend_schema_view(
    list=extend_schema(description="Get a list of all categories."),
    retrieve=extend_schema(description="Get details of a single category by it's ID."),
    create=extend_schema(description="[Admin Only] Create a new category."),
    update=extend_schema(description="[Admin Only] Fully update a category's details."),
    partial_update=extend_schema(
        description="[Admin Only] Partially update a category's details."
    ),
    destroy=extend_schema(
        description="[Admin Only] Delete a category from the catalog."
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by("name")

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()


@extend_schema_view(
    list=extend_schema(description="Get a list of the current user's past orders."),
    retrieve=extend_schema(description="Get details of a specific order."),
    create=extend_schema(
        description="Create a new order from the user's current shopping cart."
    ),
)
class OrderViewSet(viewsets.ModelViewSet):
    """
    Manages user orders. Allows creating an order (checkout) and viewing past orders.
    """

    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]  # No updates or deletes

    def get_serializer_class(self):
        if self.action == "create":
            return CreateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        # Pass the user and their cart to the serializer context
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        return {"user": user, "cart": cart}

    def get_queryset(self):
        # Users should only be able to see their own orders
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "order_items__product"
        )


@extend_schema_view(
    retrieve=extend_schema(description="Retrieve the current user's shopping cart."),
)
class CartViewSet(
    viewsets.GenericViewSet,
    generics.RetrieveAPIView,
):
    """
    A viewset that provides a `retrieve` action for the current user's cart.
    The cart is automatically created for a user if they don't have one.
    """

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve or create a cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def get_queryset(self):
        # This ensures users can only see their own cart
        return Cart.objects.filter(user=self.request.user)


@extend_schema_view(
    list=extend_schema(description="List all items in the current user's cart."),
    create=extend_schema(description="Add a product to the cart."),
    partial_update=extend_schema(
        description="Update the quantity of an item in the cart."
    ),
    destroy=extend_schema(description="Remove an item from the cart."),
)
class CartItemViewSet(viewsets.ModelViewSet):
    """
    Manages items within the current user's shopping cart.
    Allows adding, updating, and removing cart items.
    """

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]  # Limit available methods

    def get_serializer_context(self):
        """
        Passes the user's cart to the serializer as context.
        This is needed for the serializer's custom create logic.
        """
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        # Add the cart to the default context and return it
        context = super().get_serializer_context()
        context["cart"] = cart
        return context

    def get_queryset(self):
        # Filter items to only those in the user's cart
        user = self.request.user
        # Ensure a cart exists before querying items
        cart, _ = Cart.objects.get_or_create(user=user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        # Associate the new cart item with the user's cart
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
