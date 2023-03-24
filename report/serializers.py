from rest_framework import serializers, viewsets
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'date_from', 'date_to', 'orders', 'payments']


class PaidReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        queryset = Report.objects.filter(
            date_from__lte=date_to,
            date_to__gte=date_from,
            payments__status='paid'
        ).distinct()
        return queryset


class CompletedReportViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        queryset = Report.objects.filter(
            date_from__lte=date_to,
            date_to__gte=date_from,
            orders__status='completed'
        ).distinct()
        return queryset
