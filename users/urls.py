from django.urls import include, path

from users.views import CustomerViewSet, CustomTokenObtainPairView

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
    path('server/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
