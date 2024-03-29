from django.db.models import Subquery
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from core.permissions import HasShop, IsOwner
from .filters import ShopProductFilter
from products.models import Product, ProductVariant
from products.serializers import ProductSerializer, ProductVariantSerializer, SingleProductSerializer
from reviews.models import Review
from reviews.serializers import ShopReviewSerializer
from payments.models import TransferMoney
from payments.serializers import TransferMoneySerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Link, Shop
from .serializers import (
    CreateShopSerializer,
    LinkSerializer,
    ShopSerializer,
    SingleShopSerializer,
)

from django.db.models.functions import Coalesce
from django.db.models import Subquery, OuterRef, Sum, Value


@extend_schema(
    description="Viewset to edit user's shop",
    request=CreateShopSerializer,
    responses={200: SingleShopSerializer},
    tags=["Owner"],
)
class MyShopViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to edit user's shop
    available all methods
    """

    queryset = Shop.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateShopSerializer
        return SingleShopSerializer

    def perform_create(self, serializer):
        """
        On create set user to current user
        """
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Set permissions
        """
        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), HasShop()]

    def get_object(self):
        """
        Return only user's shop
        """
        return self.request.user.shop

    @extend_schema(
        description="Get shop reviews",
        responses={200: ShopReviewSerializer},
        tags=["Owner"],
    )
    @action(detail=True, methods=["get"])
    def get_shop_reviews(self, request, pk=None):
        shop = self.get_object()
        reviews = Review.objects.filter(shop=shop)
        serializer = ShopReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)


class ShopProductsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset to get all Shop products and Shop product detail
    Only to get
    """

    queryset = Shop.objects.all()
    permission_classes = [permissions.AllowAny]
    filterset_class = ShopProductFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, ]
    search_fields = ["name", "id"]
    ordering_fields = ["name", "created_at", "price"]

    @extend_schema(
        description="Get shop products",
        parameters=[OpenApiParameter("slug", OpenApiTypes.STR, OpenApiParameter.PATH)],
        responses={200: ProductSerializer},
        tags=["All"],
    )
    def products(self, request, *args, **kwargs):
        qs = Product.objects.filter(is_published=True).prefetch_related("variants")
        qs = qs.annotate(
            overall_price=Subquery(
                ProductVariant.objects.filter(product=OuterRef("pk")).values(
                    "overall_price"
                )[:1]
            ),
            discount_price=Subquery(
                ProductVariant.objects.filter(product=OuterRef("pk")).values(
                    "discount_price"
                )[:1]
            ),
            price=Subquery(
                ProductVariant.objects.filter(product=OuterRef("pk")).values(
                    "price"
                )[:1]
            ),
        )
        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SingleShopSerializer
        return ShopSerializer

    @extend_schema(
        description="Viewset to control only user's shop links",
        parameters=[OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH)],
        responses={200: LinkSerializer},
        tags=["Owner"],
    )
    @action(detail=True, methods=["get"], url_path="links")
    def list_links(self, request, id=None):
        shop = get_object_or_404(Shop, pk=id)
        links = shop.links.all()
        serializer = LinkSerializer(links, many=True)
        return Response(serializer.data)


class ShopListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    A viewset for listing all shops
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = []  # Allow any permission

    @extend_schema(
        description="Get a list of all shops",
        responses={200: ShopSerializer(many=True)},
        tags=["Shops"],
    )
    def list(self, request):
        return super().list(request)


class LinkViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset to control only user's shop links
    Maximum 5 links per shop
    """

    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated, HasShop, IsOwner]

    def perform_create(self, serializer):
        """
        On create save shop
        """
        serializer.save(shop=self.request.user.shop)

    def get_queryset(self):
        """
        Return only user's shop links
        """
        return Link.objects.filter(shop=self.request.user.shop)


class TransferMoneyViewSet(mixins.ListModelMixin):
    serializer_class = TransferMoneySerializer
    permission_classes = [permissions.IsAuthenticated, HasShop]

    def get_queryset(self):
        return TransferMoney.objects.filter(shop=self.request.user.shop)


class ShopDetailView(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        # Append full URL path to the image fields
        shop = response.data
        shop['cover_picture'] = request.build_absolute_uri(shop['cover_picture'])
        shop['profile_picture'] = request.build_absolute_uri(shop['profile_picture'])

        return response
