from rest_framework import serializers
from rest_framework.serializers import Field

from core import settings
from products.serializers import ProductSerializer
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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['cover_picture'] = self.get_cover_picture_url(instance)
        return ret

    def get_cover_picture_url(self, obj):
        if obj.cover_picture:
            return "{}{}".format(settings.MEDIA_URL, obj.cover_picture.name)
        return None

class SingleShopSerializer(serializers.ModelSerializer):
    """
    Only single shop serializer
    Return only one shop with all fields
    """

    user = CustomerSerializer(read_only=True)
    links = LinkSerializer(many=True, read_only=True)
    products = ProductSerializer(read_only=True, many=True)

    class Meta:
        model = Shop
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['cover_picture'] = self.get_cover_picture_url(instance)
        return ret

    def get_cover_picture_url(self, obj):
        if obj.cover_picture:
            return "{}{}".format(settings.MEDIA_URL, obj.cover_picture.name)
        return None


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

        def to_representation(self, instance):
            ret = super().to_representation(instance)
            ret['cover_picture'] = self.get_cover_picture_url(instance)
            return ret

        def get_cover_picture_url(self, obj):
            if obj.cover_picture:
                return "{}{}".format(settings.MEDIA_URL, obj.cover_picture.name)
            return None
