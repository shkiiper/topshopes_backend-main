from rest_framework import serializers
from rest_framework.serializers import Field

from shops.models import Shop
from shops.serializers import ShopSerializer
from .models import Address, Customer, Seller


class CreateCustomerSerializer(serializers.ModelSerializer):
    """
    Serialzier to create customer
    """

    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "password",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer Customer to read_only
    """

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "avatar",
            "is_superuser",
            "is_seller",
        ]
#
#
# class ShopNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shop
#         fields = ('name',)
#
#
# class SellerSerializer(serializers.ModelSerializer):
#     shop = ShopNameSerializer(read_only=True)
#
#     class Meta:
#         model = Customer
#         fields = [
#             "id",
#             "first_name",
#             "last_name",
#             "email",
#             "phone",
#             "avatar",
#             "is_superuser",
#             "is_seller",
#             "shop",
#         ]
#
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         if not instance.is_seller:
#             data.pop('shop')
#         return data

class CreateAddressSerializer(serializers.ModelSerializer):
    """
    Serializer to create addresses
    """

    user: Field = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = ["user", "country", "city", "street", "phone"]


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer to read only addresses
    """

    class Meta:
        model = Address
        fields = ["id", "user", "country", "city", "street", "phone"]
