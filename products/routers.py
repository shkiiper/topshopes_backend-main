from uuid import UUID

from rest_framework import routers
from django.urls import path, include

from attributes.views import AttributeValueViewset
from reviews.views import ReviewViewSet
from shops.views import ShopViewSet

from .views import (
    BrandViewSet,
    CategoryViewSet,
    ImageViewSet,
    ProductVariantViewSet,
    ProductViewSet,
    ShopProductViewSet,
)

router = routers.SimpleRouter()
# routes for authorized users
router.register(r"products/variants/images", ImageViewSet, basename="image")
router.register(
    r"products/variants/attributes", AttributeValueViewset, basename="attributes"
)
router.register(r"products/variants", ProductVariantViewSet, basename="variant")
router.register(r"products", ShopProductViewSet, basename="product")
# routes for all users
router.register(r"shops/categories", CategoryViewSet, basename="category")
router.register(r"shops/brand", BrandViewSet, basename="brand")
router.register(r"shops/products", ProductViewSet, basename="products")
urlpatterns = [
    path('', include(router.urls)),
    path('server/shops/<uuid:pk>/products/', ShopViewSet.as_view({'get': 'products'}), name='shop-products'),

]