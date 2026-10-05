from django.db import models
from branch.models import Branch
from user.models import User


class Customer(models.Model):

    branch = models.ForeignKey(
        Branch,
        related_name='customers',\
        on_delete=models.CASCADE
    )

    assigned_to = models.ForeignKey(
        User,
        related_name='customers',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    company = models.CharField(
        max_length=150,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=50
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name