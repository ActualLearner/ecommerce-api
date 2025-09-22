from django_filters import rest_framework as filters
from shop.models import Product


class ProductFilter(filters.FilterSet):

    category = filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['category']
