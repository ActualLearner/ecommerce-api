from django.db import models
from shop.models import Order, Status

# Create your models here.


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    transaction_ref = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.pending,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.chapa_tx_ref} for Order {self.order.id}"
