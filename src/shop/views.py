from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySerializer,
)
from .models import Product, Category
from .filters import ProductFilter

# Create your views here.


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


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()
