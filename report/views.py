from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from rest_framework import generics, filters
from orders.models import Order
from .models import Report
from .serializers import ReportSerializer
from rest_framework.response import Response
from django.db import models
from orders.serializers import OrderSerializer


class ReportAPIView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['total_price', 'created_at']

    def get_queryset(self):
        queryset = Report.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d')) + timedelta(days=1)
            delta = end_date - start_date
            if delta.days > 30:
                end_date = start_date + timedelta(days=30)

            queryset = queryset.filter(created_at__range=[start_date, end_date])

        return queryset

    def create(self, request, *args, **kwargs):
        orders = Order.objects.filter(status__in=['paid', 'completed'])
        total_price = orders.aggregate(models.Sum('total_price'))['total_price__sum']
        status = request.data.get('status', 'all')
        created_at = datetime.now()

        report = Report.objects.create(
            total_price=total_price or 0,
            status=status,
            created_at=created_at
        )

        serializer = self.get_serializer(report)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
