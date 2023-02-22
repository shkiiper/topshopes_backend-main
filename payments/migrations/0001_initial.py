# Generated by Django 4.1.3 on 2023-02-22 11:52

import core.helpers
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "payment_type",
                    models.CharField(
                        choices=[
                            ("elsom", "Elsom"),
                            ("visa", "Visa"),
                            ("o_dengi", "O'Dengi"),
                            ("balance", "Balance"),
                            ("mbank", "Mbank"),
                        ],
                        max_length=20,
                        verbose_name="Payment Type",
                    ),
                ),
                (
                    "confirm_photo",
                    models.ImageField(
                        upload_to=core.helpers.PathAndRename("payment/confirm_photo")
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=20, verbose_name="Phone Number"),
                ),
                (
                    "bank_account",
                    models.CharField(max_length=20, verbose_name="Bank Account"),
                ),
                (
                    "is_verified",
                    models.BooleanField(
                        blank=True, null=True, verbose_name="Is Verified"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TransferMoney",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Amount"
                    ),
                ),
                (
                    "tax",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Tax"
                    ),
                ),
                (
                    "confirm_photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=core.helpers.PathAndRename(
                            "payment/transfer/confirm_photo"
                        ),
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "payment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transfer_money",
                        to="payments.payment",
                    ),
                ),
            ],
        ),
    ]
