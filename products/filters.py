import django_filters
from django.utils import timezone
from .models import Product, Brand


class ProductFilter(django_filters.FilterSet):
    max_price = django_filters.CharFilter(field_name="price", lookup_expr="lte")
    min_price = django_filters.CharFilter(field_name="price", lookup_expr="gte")
    category = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    brand = django_filters.ModelMultipleChoiceFilter(
        field_name='brand__name',
        to_field_name='name',
        queryset=Brand.objects.all()
    )
    has_discount = django_filters.BooleanFilter(method='filter_has_discount')
    new_arrival = django_filters.BooleanFilter(method='filter_new_arrival')
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name="rating", lookup_expr='lte')

    def filter_has_discount(self, queryset, name, value):
        if value:
            return queryset.filter(variants__discount_price__isnull=False)
        return queryset

    def filter_new_arrival(self, queryset, name, value):
        if value:
            yesterday = timezone.now() - timezone.timedelta(days=2)
            queryset = queryset.filter(created_at__gte=yesterday)
        return queryset

    class Meta:
        model = Product
        fields = ["max_price", "min_price", "brand", "category", "has_discount", "new_arrival", "min_rating",
                  "max_rating"]
