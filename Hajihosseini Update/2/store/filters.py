from django_filters.rest_framework import FilterSet

from .models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'inventory': ['exact', 'lt', 'gt'],
            'unit_price': ['range', 'lte', 'gte'],
        }