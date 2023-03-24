from django_filters import rest_framework as filters
from .models import Order


class OrderFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['date_from', 'date_to']
