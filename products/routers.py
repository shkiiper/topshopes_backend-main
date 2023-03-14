from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import routers

from attributes.views import AttributeValueViewset
from .models import Product
from .serializers import ProductSerializer
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
router = routers.DefaultRouter()


class LatestProductsAPIView(APIView):
    def get(self, request):
        latest_products = Product.objects.order_by('-created_at')[:10]
        serializer = ProductSerializer(latest_products, many=True)
        return Response(serializer.data)


router.register(r'latest-products', LatestProductsAPIView, basename='latest-products')
urlpatterns = router.urls
