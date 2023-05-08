from rest_framework import serializers
from django.db.transaction import atomic

import products
from payments.models import Payment
from products.serializers import ProductSerializer, ProductVariantSerializer, CategorySerializer, \
    CategoryReadOnlySerializer
from shops.serializers import ShopSerializer
from users.models import Customer
from users.serializers import AddressSerializer, CustomerSerializer
import redis
from django.conf import settings
from redis.exceptions import LockError
from products.models import ProductVariant, Product, Category

from .models import Order


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    Return id, name, icon, image, slug, parent, description, featured fields
    """

    class Meta:
        model = Category
        fields = [
            "id",
            "slug",
            "name",
            "icon",
            "image",
            "attributes",
            "featured",
            "tax",
        ]


class OrderInfoSerializer(serializers.ModelSerializer):
    """
    Order serializers for read only
    return product and quantity
    """

    class Meta:
        model = Order
        fields = [
            "product_variant",
            "quantity",
        ]


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializers for read only
    """

    user = CustomerSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()
    shop = ShopSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)
    product = ProductSerializer(
        read_only=True, source="product_variant.product")
    address = AddressSerializer(read_only=True)
    tax = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "shop",
            "created_at",
            "total_price",
            "status",
            "delivered_at",
            "product_variant",
            "product",
            "quantity",
            "address",
            "payment",
        ]

    def get_tax(self, obj):
        """
        Вычисляет налог на основе дохода и ставки налога, учитывая специальный статус пользователя
        """
        if obj.user.special:
            tax_rate = 0.1  # установка ставки налога 10%, если пользователь имеет специальный статус
        else:
            tax_rate = 0.15  # установка ставки налога 15%, если пользователь не имеет специального статуса

        tax = obj.total_price * tax_rate  # вычисление налога на основе ставки налога и общей стоимости заказа

        return tax


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Order serializers for create only
    """

    class Meta:
        model = Order
        fields = ["shop", "user", "product_variant",
                  "quantity", "address", "payment"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0")
        return value

    def validate_payment(self, value):
        payment = Payment.objects.get(id=value.id)
        shop_id = self.initial_data.get("shop", None)
        shops = payment.orders.values_list('shop', flat=True)
        if all(shop == shop_id for shop in shops):
            return value
        raise serializers.ValidationError(
            "All orders in payment must have the same shop")

    @atomic
    def create(self, validated_data):
        r = redis.Redis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
        )
        product_variant: ProductVariant = validated_data["product_variant"]
        order = super().create(validated_data)
        lock = r.lock(f"product_variant_{product_variant.id}_quantity", timeout=1)
        try:
            if lock.acquire():
                stock = ProductVariant.objects.get(id=product_variant.id).stock
                if validated_data["quantity"] > stock:
                    raise serializers.ValidationError(
                        "Not enough stock for this product")
                product_variant.stock -= validated_data["quantity"]
                product_variant.save()

        except LockError:
            raise serializers.ValidationError("Lock error")
        finally:
            lock.release()

        return order


class OrderTotalPriceSerializer(serializers.ModelSerializer):
    profit = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_price', 'profit']

    def get_profit(self, obj):
        order_with_product_variant = Order.objects.select_related('product_variant__product').get(id=obj.id)
        category = order_with_product_variant.product_variant.product.category
        tax = category.tax
        return str(obj.total_price - ((obj.total_price / 100) * tax))
