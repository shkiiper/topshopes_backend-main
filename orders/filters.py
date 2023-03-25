from django_filters.rest_framework import FilterSet
from .models import Order
import django_filters


class OrderFilter(FilterSet):
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['date_from', 'date_to']
