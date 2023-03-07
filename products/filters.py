from django_filters import MultipleChoiceFilter
from django_filters.rest_framework import FilterSet
import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    max_price = django_filters.CharFilter(field_name="price", lookup_expr="lte")
    min_price = django_filters.CharFilter(field_name="price", lookup_expr="gte")
    brand = django_filters.MultipleChoiceFilter(field_name='brand__name', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["max_price", "min_price", "brand", "category"]