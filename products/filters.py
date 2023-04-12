from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters
import django_filters
from .models import Product, Brand, ProductVariant
from datetime import datetime, timedelta


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
        fields = ["max_price", "min_price", "brand", "category", ]


class DisroductFilter(django_filters.FilterSet):
    has_discount = filters.BooleanFilter(method='filter_has_discount')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'has_discount']

    def filter_has_discount(self, queryset, name, value):
        if value:
            return queryset.filter(variants__discount_price__isnull=False)
        return queryset


class NewProductFilter(django_filters.FilterSet):
    new_arrival = filters.BooleanFilter(method='filter_new_arrival')

    def filter_new_arrival(self, queryset, name, value):
        if value:
            yesterday = datetime.now() - timedelta(days=2)
            queryset = queryset.filter(created_at__gte=yesterday)
        return queryset

    class Meta:
        model = Product
        fields = ['category', 'brand', 'new_arrival']


class RatProductFilter(django_filters.FilterSet):
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'brand', 'min_rating', 'max_rating']
