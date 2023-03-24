from django.db import models
from django.utils import timezone


class Report(models.Model):
    date_from = models.DateTimeField(null=True, blank=True)
    date_to = models.DateTimeField(null=True, blank=True)
    orders = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="report")
    # payments = models.ForeignKey("payments.Payment", on_delete=models.CASCADE, related_name="report")