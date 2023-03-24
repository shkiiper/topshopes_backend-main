from rest_framework import routers
from .views import ReportViewSet

router = routers.DefaultRouter()
router.register(r'report', ReportViewSet, basename='report')

urlpatterns = router.urls
