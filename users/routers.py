from rest_framework import routers
from .views import AddressViewSet, CustomerViewSet
from payments.views import UserPaymentViewSet

router = routers.SimpleRouter()

router.register(r"address", AddressViewSet, basename="address")
router.register(r"payments", UserPaymentViewSet, basename="payment")
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'sellers', CustomerViewSet, basename='sellers')
