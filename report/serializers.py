from rest_framework import serializers
from orders.models import Order
from .models import Report


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Report
        fields = '__all__'
