from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='orders.total_price')

    class Meta:
        model = Report
        fields = ['id', 'date_from', 'date_to', 'total_price']
