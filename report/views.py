from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ReportSerializer
from .models import Report


class PaidOrderList(ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        queryset = Report.objects.filter(payments__status=self.request.query_params.get('status', 'paid'))
        if date_from:
            queryset = queryset.filter(date_to__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_from__lte=date_to)
        return queryset


class CompletedOrderList(ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        queryset = Report.objects.filter(orders__status=self.request.query_params.get('status', 'completed'))
        if date_from:
            queryset = queryset.filter(date_to__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_from__lte=date_to)
        return queryset
