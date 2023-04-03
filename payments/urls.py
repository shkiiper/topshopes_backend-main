from django.urls import include, path
from .views import ReportAdmin, ReportClient

urlpatterns = [
    path("report-admin/", ReportAdmin.as_view()),
    path("report-client/", ReportClient.as_view()),
]