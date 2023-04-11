from django_filters.rest_framework import FilterSet
import django_filters
from django.db.models import Sum, Subquery, OuterRef
from rest_framework import viewsets
from .models import Product, Brand, ProductVariant
from .serializers import ProductSerializer


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


def filter_best_selling_products(request):
    best_selling_view = BestSellingProductViewSet.as_view({'get': 'list'})
    best_selling_products = best_selling_view(request).data

    filtered_products = ProductFilter(
        data=request.GET,
        queryset=Product.objects.filter(id__in=[p['id'] for p in best_selling_products])
    ).qs

    return filtered_products


class BestSellingProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View set to retrieve best selling products
    """
    queryset = (
        Product.objects.filter(is_published=True)
        .annotate(
            price=Subquery(
                ProductVariant.objects.filter(
                    product=OuterRef("pk")
                ).values("price")[:1]
            ),
            total_sales=Sum("variants__orders__quantity"),
        )
        .order_by("-total_sales")
    )
    serializer_class = ProductSerializer
