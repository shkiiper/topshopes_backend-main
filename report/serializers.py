from rest_framework import serializers
from orders.models import Order
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'orders', 'date_from', 'date_to')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status')


class OrderInReportSerializer(OrderSerializer):
    in_report = serializers.BooleanField()


class ReportDetailSerializer(ReportSerializer):
    orders = OrderInReportSerializer(many=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        orders = representation.pop('orders')
        for order in orders:
            order['in_report'] = True
        representation['orders'] = orders
        return representation
