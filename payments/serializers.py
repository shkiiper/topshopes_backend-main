from django.db.models import Sum
from orders.models import Order
from shops.models import Shop

from rest_framework import serializers
from orders.serializers import OrderSerializer
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
    profit = serializers.SerializerMethodField()

    class Meta:
        model = TransferMoney
        fields = ["id", "payment", "amount", "shop", "tax", "confirm_photo", "profit"]

    # def get_profit(self, obj):
    #     order_with_product_variant = Order.objects.select_related('product_variant__product').get(id=obj.id)
    #     category = order_with_product_variant.product_variant.product.category
    #     tax = category.tax
    #     return str(obj.total_price - ((obj.total_price / 100) * tax))
    def get_profit(self, obj):
        order = Order.objects.select_related('product_variant__product__category').get(id=obj.id)
        shop_status = obj.shop.status
        if shop_status == "special":
            tax = order.product_variant.product.category.special_tax
        else:
            tax = order.product_variant.product.category.tax

        return str(obj.total_price - ((obj.total_price / 100) * tax))


class ReportSerializer(serializers.ModelSerializer):
    total_tax = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'name', 'total_tax', 'total_amount']

    def get_total_tax(self, obj):
        year = self.context['request'].data.get('year')
        month = self.context['request'].data.get('month')
        return obj.transfermoney_set.filter(
            created_at__year=year,
            created_at__month=month
        ).aggregate(Sum('tax'))['tax__sum']

    def get_total_amount(self, obj):
        year = self.context['request'].data.get('year')
        month = self.context['request'].data.get('month')
        return obj.transfermoney_set.filter(
            created_at__year=year,
            created_at__month=month).aggregate(Sum('amount'))['amount__sum']
