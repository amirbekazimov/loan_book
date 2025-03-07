from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_shop_owner = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_creditor = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, unique=True)


class Debt(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="debts")
    creditor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="creditor_debts")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.customer.username} owes {self.amount} to {self.creditor.username} - {'Paid' if self.is_paid else 'Not Paid'}"
