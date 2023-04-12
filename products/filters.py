from django_filters.rest_framework import FilterSet
import django_filters
from .models import Product, Brand, ProductVariant


class ProductFilter(FilterSet):
    max_price = django_filters.CharFilter(field_name="price", lookup_expr="lte")
    min_price = django_filters.CharFilter(field_name="price", lookup_expr="gte")
    category = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    brand = django_filters.ModelMultipleChoiceFilter(
        field_name='brand__name',
        to_field_name='name',
        queryset=Brand.objects.all()
    )

    class Meta:
        model = Product
        fields = ["max_price", "min_price", "brand", "category"]


class ProductFilter(django_filters.FilterSet):
    is_discounted = django_filters.BooleanFilter(
        field_name='variants__discount_price',
        lookup_expr='isnull',
        exclude=True
    )

    class Meta:
        model = Product
        fields = ['category', 'brand', 'is_discounted']


class ProductFilter(django_filters.FilterSet):
    is_new = django_filters.BooleanFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='New Products'
    )

    class Meta:
        model = Product
        fields = ['category', 'brand', 'is_new']


class ProductFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(
        field_name='rating',
        lookup_expr='gte',
        label='Minimum Rating'
    )

    class Meta:
        model = Product
        fields = ['category', 'brand', 'rating']
