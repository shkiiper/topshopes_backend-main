import django_filters
from django.utils import timezone
from django.db.models import OuterRef, Subquery
from .models import Product, Brand, ProductVariant
from django.db.models import F

from .serializers import ProductVariantSerializer


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
    serializer_class = ProductVariantSerializer

    def filter_has_discount(self, queryset, name, value):
        queryset = (
            Product.objects.filter(variants__discount__gt=0, is_published=True)
            .annotate(
                discounted_price=F("variants__price") - (F("variants__price") * F("variants__discount") / 100),
                price_annotation=F("variants__price"),
            )
            .order_by("-discounted_price")
        )
        return queryset

    def filter_new_arrival(self, queryset, name, value):
        queryset = (
            Product.objects.all()
            .prefetch_related("variants")
            .annotate(
                price=Subquery(
                    ProductVariant.objects.filter(product=OuterRef("pk")).values(
                        "price"
                    )[:1]
                )
            )
        )
        return queryset

    class Meta:
        model = Product
        fields = ["max_price", "min_price", "brand", "category", "has_discount", "new_arrival", "min_rating",
                  "max_rating"]
