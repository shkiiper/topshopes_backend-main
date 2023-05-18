from rest_framework import serializers
from rest_framework.serializers import Field

import products.serializers
from attributes.serializers import AttributeSerializer, AttributeValueSerializer
from orders.models import Order
from django.db.models import Sum
from products.models import Brand, BrandType, Category, Image, Product, ProductVariant
from reviews.serializers import ReviewSerializer
from shops.models import Shop


class ShopProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["id", "name", "slug"]


class BrandSerializer(serializers.ModelSerializer):
    """
    Brand serializer able to select fields to represent
    Return all fields
    """

    slug = serializers.ReadOnlyField()

    class Meta:
        model = Brand
        fields = "__all__"


class BrandTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for brand type
    Return all fields
    """

    class Meta:
        model = BrandType
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for product image
    Return only id and image
    """

    class Meta:
        model = Image
        fields = ["id", "image", "product_variant"]


class CreateCategorySerializer(serializers.ModelSerializer):
    """
    Serialzier to create category only
    """

    tax = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Category
        fields = [
            "name",
            "description",
            "icon",
            "image",
            "attributes",
            "tax",
        ]


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    Return id, name, icon, image, slug, parent, description, featured fields
    """

    slug = serializers.ReadOnlyField()

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

    def get_tax(self, tax=None):
        if Product.shop.status == "special":
            return '10.00'
        return tax


class CategoryReadOnlySerializer(serializers.ModelSerializer):
    """
    Category serializer
    Return id, name
    """

    class Meta:
        model = Category
        fields = ["id", "name", "tax"]


class CreateProductVariantSerializer(serializers.ModelSerializer):
    """
    Product variant serializer for write only
    Return all fields
    """

    id = serializers.ReadOnlyField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "price",
            "discount",
            "thumbnail",
            "stock",
            "status",
            'ordering'
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Product variant serializer for read only
    Return all fields
    """

    images = ImageSerializer(many=True, read_only=False)
    # Устанавливаем поле 'thumbnail' в режим не только для чтения
    thumbnail = serializers.ImageField(read_only=False)
    attribute_values = AttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "price",
            "overall_price",
            "discount",
            "discount_price",
            "stock",
            "status",
            "thumbnail",
            "attribute_values",
            "images",
            'ordering',
        ]


class CreateProductSerializer(serializers.ModelSerializer):
    """
    Product serializer for write only
    Return all fields
    """

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "brand",
            "unit",
            "featured",
            "is_published",
        ]


class BrandReadSerializer(serializers.ModelSerializer):
    """
    Brand return only id, slug, name
    """

    class Meta:
        model = Brand
        fields = ["id", "slug", "name"]


class SingleProductSerializer(serializers.ModelSerializer):
    """
    Single Product serializer for read only
    """

    variants = ProductVariantSerializer(many=True, read_only=True)
    attributes = AttributeSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    shop = ShopProductSerializer(read_only=True)
    brand = BrandReadSerializer(read_only=True)
    category = CategoryReadOnlySerializer(read_only=True)
    discount_price = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )
    sold_quantity = serializers.SerializerMethodField()

    def get_sold_quantity(self, product):
        # Получаем общее количество проданных товаров для данного продукта
        sold_quantity = Order.objects.filter(product_variant__product=product).aggregate(Sum('quantity'))[
            'quantity__sum']
        return sold_quantity or 0

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "name",
            "shop",
            "description",
            "category",
            "rating",
            "brand",
            "unit",
            "featured",
            "variants",
            "reviews",
            "attributes",
            'created_at',
            "is_published",
            "discount_price",
            "sold_quantity",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer
    """

    shop = ShopProductSerializer(read_only=True)
    category: Field = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all()
    )
    overall_price = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )
    discount_price = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )
    discount = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    thumbnail = serializers.SerializerMethodField()
    brand = serializers.SlugRelatedField(
        slug_field="name", queryset=Brand.objects.all()
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "name",
            "shop",
            "category",
            "rating",
            "overall_price",
            "discount_price",
            "brand",
            "discount",
            "thumbnail",
            "price",
            'created_at',
            'is_published',
        ]

    def get_thumbnail(self, object):
        variant = object.variants.first().thumbnail
        return self.context["request"].build_absolute_uri(variant.url)


class SingleCategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    Return id, name, icon, image, slug, parent, description, featured fields
    """

    attributes = AttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "icon",
            "image",
            "slug",
            "parent",
            "description",
            "featured",
            "attributes",
            "tax",
        ]
