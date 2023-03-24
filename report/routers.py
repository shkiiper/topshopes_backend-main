from django.urls import path
from rest_framework import routers
from .views import ReportAPIView

router = routers.SimpleRouter()
router.register(r'report', ReportAPIView, basename='report')

urlpatterns = router.urls
