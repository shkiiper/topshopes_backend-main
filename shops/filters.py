from django_filters.rest_framework import FilterSet
import django_filters

from products.models import Brand
from .models import Shop


class ShopProductFilter(FilterSet):
    max_price = django_filters.CharFilter(field_name="products__ProductVariant__price", lookup_expr="lte")
    min_price = django_filters.CharFilter(field_name="products__ProductVariant__price", lookup_expr="gte")
    category = django_filters.CharFilter(field_name="products__category__name", lookup_expr="icontains")
    brand = django_filters.ModelMultipleChoiceFilter(
        field_name='products__brand__name',
        to_field_name='name',
        queryset=Brand.objects.all()
    )

    class Meta:
        model = Shop
        fields = ["max_price", "min_price", "category", "brand", ]