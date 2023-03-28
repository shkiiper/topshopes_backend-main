from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from core.permissions import IsAnonymous

from .models import Address, Customer
from .serializers import (
    AddressSerializer,
    CreateAddressSerializer,
    CreateCustomerSerializer,
    CustomerSerializer,
)


@extend_schema(
    description="CustomerViewSet to create,update and retrieve current user",
    responses={200: CustomerSerializer},
    tags=["Owner"],
)
class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    Viewset to create,update and retrieve current user
    """

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CustomerSerializer
        return CreateCustomerSerializer

    def get_permissions(self):
        """
        Create available only for anonymous users
        """
        if self.action == "create":
            self.permission_classes = [IsAnonymous]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """
        If user is authenticated return only current user
        """
        return Customer.objects.all().filter(id=self.request.user.id)

    def get_object(self, pk=None):
        return self.request.user

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.data["password"]))


@extend_schema(
    description="Address Viewset allowed all methods",
    request=CreateAddressSerializer,
    responses={200: AddressSerializer},
    tags=["Owner"],
)
class AddressViewSet(ModelViewSet):
    """
    Address Viewset allowed all methods
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        return Address.objects.all().filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CreateAddressSerializer
        return AddressSerializer


# Import data

import json
from django.core.management.base import BaseCommand
from products.models import Product, Category, Brand, ProductVariant, Image


class Command(BaseCommand):
    help = 'Import data from JSON file to Django database'

    def add_arguments(self, parser):
        parser.add_argument('import.json', type=str, help='JSON filename')

    def handle(self, *args, **options):
        filename = options['import.json']

        with open(filename) as file:
            data = json.load(file)

        for product_data in data:
            # Create or update category
            category_name = product_data.pop('category')
            category, created = Category.objects.get_or_create(name=category_name,
                                                               defaults=product_data.pop('category_data'))

            # Create or update brand
            brand_name = product_data.pop('brand')
            brand, created = Brand.objects.get_or_create(name=brand_name, defaults=product_data.pop('brand_data'))

            # Create product
            product = Product.objects.create(category=category, brand=brand, **product_data)

            # Create product variants
            variants_data = product_data.pop('variants')
            for variant_data in variants_data:
                variant = ProductVariant.objects.create(product=product, **variant_data)

            # Create product images
            images_data = product_data.pop('images')
            for image_data in images_data:
                image = Image.objects.create(product_variant=variant, **image_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {filename}'))
