# report/views.py
from rest_framework import viewsets
from rest_framework import filters
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Report
from .serializers import ReportSerializer, OrderSerializer


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        # Filter by date range
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if date_from and date_to:
            date_from = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
            date_to = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d'))
            if date_to - date_from > timedelta(days=30):
                date_from = date_to - timedelta(days=30)
            queryset = queryset.filter(created_at__range=[date_from, date_to])

        return queryset
