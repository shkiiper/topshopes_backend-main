from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # swagger
    path("server/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "server/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "server/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # django admin
    path("admin/", admin.site.urls),
    # website admin's routes
    path("server/admin/", include("head.urls"), name="admin_base_API"),
    # app routes
    path("server/", include("users.urls"), name="users_base_API"),
    path("server/", include("orders.urls"), name="orders_base_API"),
    path("server/", include("products.urls"), name="products_base_API"),
    path("server/", include("reviews.urls"), name="reviews_base_API"),
    path("server/", include("shops.urls"), name="shops_base_API"),
    path("server/", include("posts.urls"), name="posts_base_API"),
    path("server/", include("payments.urls"), name="payments_base_API"),
    # path("api/", include("attributes.urls"), name="attributes_base_API"),
    # auth routes
    path("server/auth/login/", TokenObtainPairView.as_view(), name="token_create"),
    path("server/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # pages routes
    path("server/", include("pages.urls"), name="pages_base_API"),
    # sliders routes
    path("server/", include("sliders.urls"), name="sliders_base_API"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
