import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone


class Order(models.Model):
    """
    Model of order
    Contains one product information
    """

    STATUSES = (
        ("payment_error", "Payment Error"),
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("ready", "Ready"),
        ("shop_decline", "Shop Decline"),
        ("delivering", "Delivering"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
        ("completed", "Completed"),
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(
        "users.Customer", on_delete=models.CASCADE, related_name="orders"
    )
    payment = models.ForeignKey(
        "payments.Payment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    shop = models.ForeignKey(
        "shops.Shop", on_delete=models.CASCADE, related_name="orders"
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal(0.00)
    )
    quantity = models.IntegerField(default=1)
    product_variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(max_length=20, choices=STATUSES, default="pending")
    address = models.ForeignKey(
        "users.Address", on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.shop}"

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # self.total_price = self.product_variant.discount_price * self.quantity
        if self.product_variant.discount_price == 0:
            self.total_price = self.product_variant.price * self.quantity
        else:
            self.total_price = self.product_variant.discount_price * self.quantity

        if self.status == "delivered":
            self.delivered_at = timezone.now()
        if self.status == "paid":
            from payments.models import TransferMoney

            # tax = self.product_variant.tax_price * self.quantity
            tax = (self.product_variant.price - self.product_variant.overall_price) * self.quantity
            TransferMoney.objects.create(
                payment=self.payment,
                shop=self.shop,
                amount=self.total_price,
                tax=tax,
            )
        if self.status == "payment_error":
            self.payment.money_transfer.delete()
        super().save(*args, **kwargs)