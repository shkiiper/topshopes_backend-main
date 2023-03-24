from rest_framework import routers

from orders.views import OrderViewSet, OrderList

router = routers.SimpleRouter()
router.register(r"orders", OrderList, basename="orders")
router.register(r'orderList', OrderList, basename='orderList')