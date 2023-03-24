from django.urls import path, include
from rest_framework import routers
from .views import PaidOrderList, CompletedOrderList

router = routers.DefaultRouter()
router.register(r'orders/paid', PaidOrderList, basename='paid-orders')
router.register(r'orders/completed', CompletedOrderList, basename='completed-orders')

urlpatterns = [
    path('', include(router.urls)),
]