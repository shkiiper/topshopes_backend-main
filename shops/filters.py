from django_filters.rest_framework import FilterSet
import django_filters
from .models import Shop


class ShopProductFilter(FilterSet):
    max_price = django_filters.CharFilter(field_name="products__ProductVariant__price", lookup_expr="lte")
    min_price = django_filters.CharFilter(field_name="products__ProductVariant__price", lookup_expr="gte")
    category = django_filters.CharFilter(field_name="products__category__name", lookup_expr="icontains")

    class Meta:
        model = Shop
        fields = ["max_price", "min_price", "category"]
