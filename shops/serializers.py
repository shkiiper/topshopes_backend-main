from rest_framework import serializers
from rest_framework.serializers import Field

from products.serializers import ProductSerializer, ProductVariantSerializer
from users.serializers import CustomerSerializer

from .models import Link, Shop


class LinkSerializer(serializers.ModelSerializer):
    """
    Serializer for create link to shop only
    Return name and link
    """

    class Meta:
        model = Link
        fields = ["id", "name", "link"]

    def create(self, validated_data):
        if Link.objects.filter(shop=validated_data["shop"]).count() > 5:
            raise serializers.ValidationError("Can't create more than 5 links pre shop")

        return super().create(validated_data)


class ShopSerializer(serializers.ModelSerializer):
    """
    Shop serializer
    Return all fields
    """

    user = CustomerSerializer()

    class Meta:
        model = Shop
        fields = "__all__"


class SingleShopSerializer(serializers.ModelSerializer):
    """
    Only single shop serializer
    Return only one shop with all fields
    """

    user = CustomerSerializer(read_only=True)
    links = LinkSerializer(many=True, read_only=True)
    products = ProductSerializer(read_only=True, many=True)
    variants = ProductVariantSerializer(read_only=True, many=True)
    price = ProductVariantSerializer(read_only=True, many=True)
    name = ProductSerializer(read_only=True)
    category = ProductSerializer(read_only=True)
    rating = ProductSerializer(read_only=True)
    discount_price = ProductVariantSerializer(read_only=True)
    brand = ProductSerializer(read_only=True)
    thumbnail = ProductSerializer(read_only=True)
    created_at = ProductSerializer(read_only=True)
    is_published = ProductSerializer(read_only=True)

    class Meta:
        model = Shop
        fields = ["id", "user", "links", "products", "variants", "price", "name", "category", "rating", "discount_price", "brand", "thumbnail", "created_at", "is_published",]


class CreateShopSerializer(serializers.ModelSerializer):
    """
    Serialize used to create shop only
    Return only one shop with all fields
    """

    user: Field = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Shop
        fields = [
            "name",
            "email",
            "user",
            "address",
            "phone",
            "cover_picture",
            "profile_picture",
        ]
