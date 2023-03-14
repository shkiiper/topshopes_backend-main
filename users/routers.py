from rest_framework import routers
from .views import AddressViewSet, UserViewSet
from payments.views import UserPaymentViewSet

router = routers.SimpleRouter()

router.register(r"address", AddressViewSet, basename="address")
router.register(r"payments", UserPaymentViewSet, basename="payment")
router.register(r'change_password', UserViewSet, basename='change_password')