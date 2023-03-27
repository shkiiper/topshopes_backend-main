from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import HasShop, IsOwner

from .serializers import OrderSerializer, CreateOrderSerializer, OrderTotalPriceSerializer

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order

from django.utils.dateparse import parse_date
from rest_framework import filters
from .filters import OrderFilter


@extend_schema(
    description="Create order",
    parameters=[
        OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH),
    ],
    request=CreateOrderSerializer,
    responses={201: OrderSerializer},
    tags=["Orders"],
)
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Viewset for user orders
    Allow to get and create only
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        """
        On get method return only current user's orders
        """
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return OrderSerializer


@extend_schema(
    description="Viewset for Shop's orders",
    parameters=[
        OpenApiParameter("id", OpenApiTypes.UUID, OpenApiParameter.PATH),
    ],
    responses={200: OrderSerializer},
    tags=["Orders"],
)
class ShopOrderViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    """
    Viewset for Shop's orders
    Can update and get only
    """

    permission_classes = (permissions.IsAuthenticated, HasShop, IsOwner)

    def get_queryset(self):
        """
        Only current user's shop orders
        """
        return (
            Order.objects.all()
            .filter(shop=self.request.user.shop)
            .exclude(status__in=["payment_error", "pending"])
        )

    def get_serializer_class(self):
        if self.action == "create":
            return CreateOrderSerializer(context={"request": self.request})
        return OrderSerializer


class OrderList(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False)
    def paid(self, request):
        queryset = self.get_queryset().filter(status='paid')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from and date_to:
            # parse dates from query parameters
            date_from = parse_date(date_from)
            date_to = parse_date(date_to)
            # filter orders by status and date range
            queryset = queryset.filter(created_at__range=(date_from, date_to))
        serializer = OrderTotalPriceSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def completed(self, request):
        queryset = self.get_queryset().filter(status='completed')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from and date_to:
            # parse dates from query parameters
            date_from = parse_date(date_from)
            date_to = parse_date(date_to)
            # filter orders by status and date range
            queryset = queryset.filter(created_at__range=(date_from, date_to))
        serializer = OrderTotalPriceSerializer(queryset, many=True)
        return Response(serializer.data)

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from and date_to:
            # parse dates from query parameters
            date_from = parse_date(date_from)
            date_to = parse_date(date_to)
            # filter orders by date range
            queryset = queryset.filter(created_at__range=(date_from, date_to))
        return queryset
