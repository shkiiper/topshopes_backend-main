from django_filters.rest_framework import FilterSet
import django_filters
from .models import Product, Brand


class ProductFilter(FilterSet):
    max_price = django_filters.CharFilter(field_name="price", lookup_expr="lte")
    min_price = django_filters.CharFilter(field_name="price", lookup_expr="gte")
    # brand = django_filters.CharFilter(field_name='brand__name', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    brand = django_filters.ModelMultipleChoiceFilter(
        field_name='brand__name',
        to_field_name='name',
        queryset=Brand.objects.all()
    )

    class Meta:
        model = Product
        fields = ["max_price", "min_price", "brand", "category"]
