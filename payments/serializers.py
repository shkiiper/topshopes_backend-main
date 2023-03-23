from django.db.models import Sum
from rest_framework import serializers
from datetime import datetime

from head.serializers import AdminShopSerializer
from orders.serializers import OrderSerializer
from shops.models import Shop
from .models import Payment, TransferMoney

from rest_framework import serializers
from orders.serializers import OrderSerializer, OrderInfoSerializer
from .models import Payment, TransferMoney
from head.serializers import AdminShopSerializer


class CreatePaymentSerialzier(serializers.ModelSerializer):
    """
    Payment serialzier to create only
    """

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_type",
            "confirm_photo",
            "phone_number",
            "bank_account",
            "create_at",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment serialzier to read only
    """

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_type",
            "phone_number",
            "bank_account",
            "is_verified",
            "create_at",
        ]


class SinglePaymentSerializer(serializers.ModelSerializer):
    """
    Payment serialzier to read only
    """

    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_type",
            "confirm_photo",
            "phone_number",
            "bank_account",
            "is_verified",
            "orders",
            "create_at",
        ]


class CreateTransferMoneySerializer(serializers.ModelSerializer):
    """
    TransferMoney serialzier to create only
    """

    class Meta:
        model = TransferMoney
        fields = ["id", "amount", "shop", "tax"]


class TransferMoneySerializer(serializers.ModelSerializer):
    """
    TransferMoney serialzier to read only
    """
    shop = AdminShopSerializer(read_only=True)

    class Meta:
        model = TransferMoney
        fields = ["id", "payment", "amount", "shop", "tax", "confirm_photo"]


# class ReportSerializer(serializers.ModelSerializer):
#     total_tax = serializers.SerializerMethodField()
#     total_amount = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Shop
#         fields = ['id', 'name', 'total_tax', 'total_amount']
#
#     def get_total_tax(self, obj):
#         year = self.context['request'].data.get('year')
#         month = self.context['request'].data.get('month')
#         return obj.transfermoney_set.filter(
#             created_at__year=year,
#             created_at__month=month
#         ).aggregate(Sum('tax'))['tax__sum']
#
#     def get_total_amount(self, obj):
#         year = self.context['request'].data.get('year')
#         month = self.context['request'].data.get('month')
#         return obj.transfermoney_set.filter(
#             created_at__year=year,
#             created_at__month=month).aggregate(Sum('amount'))['amount__sum']

class ReportSerializer(serializers.ModelSerializer):
    total_tax = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'total_tax', 'total_amount']

    def get_total_tax(self, obj):
        transfer_money_qs = obj.transfermoney_set.all()
        years = transfer_money_qs.datetimes('created_at', 'year', order='DESC')
        if years:
            year = years[0].year
            return transfer_money_qs.filter(created_at__year=year).aggregate(Sum('tax'))['tax__sum']
        return None

    def get_total_amount(self, obj):
        transfer_money_qs = obj.transfermoney_set.all()
        years = transfer_money_qs.datetimes('created_at', 'year', order='DESC')
        if years:
            year = years[0].year
            return transfer_money_qs.filter(created_at__year=year).aggregate(Sum('amount'))['amount__sum']
        return None
