from rest_framework import routers

from attributes.views import AttributeValueViewset

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
router.register(r"shop/categories", CategoryViewSet, basename="category")
router.register(r"shop/brand", BrandViewSet, basename="brand")
router.register(r"shop/products", ProductViewSet, basename="products")
