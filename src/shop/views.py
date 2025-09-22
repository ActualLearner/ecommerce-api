from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductListSerializer, ProductDetailSerializer, CategorySerializer
from .models import Product, Category
from .filters import ProductFilter

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all().select_related('category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

        return ProductDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
