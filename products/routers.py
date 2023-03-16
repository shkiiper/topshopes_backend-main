from rest_framework import routers

from attributes.views import AttributeValueViewset

from .views import (
    BrandViewSet,
    CategoryViewSet,
    ImageViewSet,
    ProductVariantViewSet,
    ProductViewSet,
    ShopProductViewSet,
    LatestProductsAPIView, TopratedproductsAPIView, DiscountedProductView, BestSellingProductViewSet
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
router.register('latest-products', LatestProductsAPIView, basename='latest-products')
router.register('top-rated-products', TopratedproductsAPIView, basename='top-rated-products')
router.register('discounted-products', DiscountedProductView, basename='discounted-products')
router.register(r'best-selling-products', BestSellingProductViewSet, basename='best-selling-products')