from django.urls import include, path
from .views import ReportAdmin, ReportClient, PaymentFilter

urlpatterns = [
    path("report-admin/", ReportAdmin.as_view()),
    path("report-client/", ReportClient.as_view()),
    path("payment-filter/", PaymentFilter.as_view()),
]