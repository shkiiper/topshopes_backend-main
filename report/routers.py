from rest_framework import routers
from .views import PaidReportList, CompletedReportList

router = routers.SimpleRouter()
router.register(r'orders/paid', PaidReportList, basename='paid-orders')
router.register(r'orders/completed', CompletedReportList, basename='completed-orders')