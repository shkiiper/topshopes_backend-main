from rest_framework import routers
from orders.views import ShopOrderViewSet
from .views import (
    ShopListViewSet,
    LinkViewSet,
    ShopProductAPIView,
)

router = routers.SimpleRouter()
# routes for authorized users
router.register(r"shop/link", LinkViewSet, basename="shop-link")
router.register(r"shop/orders", ShopOrderViewSet, basename="shop-order")
# routes for all users
router.register(r"shops", ShopListViewSet, basename="shops")
router.register(r"shops", ShopProductAPIView, basename="shops-products")
