from django.urls import include, path

from users.views import CustomerViewSet, CustomTokenObtainPairView, CustomAuthToken

from .routers import router

urlpatterns = [
    path(
        "profile/",
        CustomerViewSet.as_view(
            {
                "get": "retrieve",
                "post": "create",
                "put": "update",
                "patch": "partial_update",
            }
        ),
        name="profile",
    ),
    path("profile/", include("applications.urls")),
    path("profile/", include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view())
]
