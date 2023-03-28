from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from core.permissions import IsAnonymous
from rest_framework import viewsets
from rest_framework.response import Response

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


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('is_seller') == 'true':
            queryset = queryset.filter(is_seller=True)
        elif self.request.query_params.get('is_seller') == 'false':
            queryset = queryset.filter(is_seller=False)
        return queryset

    def create(self, request, *args, **kwargs):
        return Response(status=405)

    def update(self, request, *args, **kwargs):
        return Response(status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=405)

    def destroy(self, request, *args, **kwargs):
        return Response(status=405)