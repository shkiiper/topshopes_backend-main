from rest_framework import viewsets, mixins, permissions, status
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from calendar import monthrange

from shops.models import Shop
from .serializers import (
    CreatePaymentSerialzier,
    PaymentSerializer,
    SinglePaymentSerializer, ReportSerializer,
)
from .models import Payment, TransferMoney


@extend_schema(
    responses={200: PaymentSerializer(many=True)},
    request=CreatePaymentSerialzier,
    tags=["Owner"],
)
class UserPaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    List payments
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SinglePaymentSerializer
        if self.action == "create":
            return CreatePaymentSerialzier
        super().get_serializer_class()
        return PaymentSerializer


@extend_schema(
    responses={200: PaymentSerializer(many=True)},
    request=CreatePaymentSerialzier,
    tags=["admin"],
)
class AdminPaymentViewSet(viewsets.ModelViewSet):
    """Admin payment viewset"""

    permission_classses = [permissions.IsAdminUser]
    queryset = Payment.objects.all()

    def update(self, request, *args, **kwargs):
        if request.data.get("is_verified"):
            payment = self.get_object()
            payment.orders.update(status="paid")
        else:
            payment = self.get_object()
            payment.orders.update(status="payment_error")
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SinglePaymentSerializer
        if self.action == "create":
            return CreatePaymentSerialzier
        return PaymentSerializer


class AdminMoneyTransferViewSet(viewsets.ModelViewSet):
    """Admin money transfer viewset"""

    permission_classses = [permissions.IsAdminUser]
    queryset = TransferMoney.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SinglePaymentSerializer
        if self.action == "create":
            return CreatePaymentSerialzier
        return PaymentSerializer


class ReportAdmin(APIView):
    def post(self, request):
        if self.request.user.is_superuser or self.request.user.is_staff:
            month = request.data.get('month', '')
            year = request.data.get('year', '')
            serializer = ReportSerializer(Shop.objects.all(), many=True, context={'request': request})
            return Response(serializer.data)
        return Response(data={"You are not authorized!!!"}, status=status.HTTP_401_UNAUTHORIZED)


class ReportClient(APIView):
    def post(self, request):
        month = request.data.get('month', '')
        year = request.data.get('year', '')

        if not self.request.user.is_authenticated:
            return Response(data='User not authorized!!!', status=status.HTTP_401_UNAUTHORIZED)

        if not self.request.user.shop:
            return Response(data='User has not shop!!!', status=status.HTTP_404_NOT_FOUND)

        if not (month and year):
            return Response(data='Month and year is required fields!!!', status=status.HTTP_400_BAD_REQUEST)

        data = []
        days_of_month = monthrange(year, month)[1]
        print(days_of_month, 'asdfasjdfbkajsbdfasjdbf')
        for i in range(1, days_of_month):
            dict_data = {
                'day': i,
                'name': self.request.user.shop.name,
                'total_amount': TransferMoney.objects.filter(shop_id=self.request.user.shop.id,
                                                             created_at__year=year,
                                                             created_at__month=month,
                                                             created_at__day=i
                                                             ).aggregate(Sum('amount'))['amount__sum'],
                'total_tax': TransferMoney.objects.filter(shop_id=self.request.user.shop.id,
                                                          created_at__year=year,
                                                          created_at__month=month,
                                                          created_at__day=i
                                                          ).aggregate(Sum('tax'))['tax__sum'],
            }
            data.append(dict_data)
        return Response(data=data, status=status.HTTP_200_OK)
