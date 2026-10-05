from django.db import models

from customer.models import Customer
from user.models import User


class Lead(models.Model):

    assigned_to = models.ForeignKey(
        User,
        related_name="leads",
        on_delete=models.CASCADE
    )

    customer = models.ForeignKey(
        Customer,
        related_name="leads",
        on_delete=models.CASCADE
    )

    source = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)

    expected_value = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    expected_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    

