from django.db import models


class Report(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.status} order for {self.total_price} created at {self.created_at}"
