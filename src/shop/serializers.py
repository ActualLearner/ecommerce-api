from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class ProductListSerializer(serializers.ModelSerializer):
    # Use a simpler representation for the category in lists
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'category']


class ProductDetailSerializer(serializers.ModelSerializer):
    # The full nested representation for detail views
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        # The full list of fields
        fields = ['id', 'name', 'description', 'price',
                  'stock', 'category']


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "category", "name",
                  "description", "stock", "price"]
