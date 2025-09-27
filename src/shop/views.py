from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySerializer,
)
from .models import Product, Category
from .filters import ProductFilter

# Create your views here.

@extend_schema_view(
    list=extend_schema(description="Get a paginated list of all products. Can be filtered by category slug."),
    retrieve=extend_schema(description="Get details of a single product by it's ID."),
    create=extend_schema(description="[Admin Only] Create a new product."),
    update=extend_schema(description="[Admin Only] Fully update a product's details."),
    partial_update=extend_schema(description="[Admin Only] Partially update a product's details."),
    destroy=extend_schema(description="[Admin Only] Delete a product from the catalog."),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related("category")
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

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
    partial_update=extend_schema(description="[Admin Only] Partially update a category's details."),
    destroy=extend_schema(description="[Admin Only] Delete a category from the catalog."),
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()
