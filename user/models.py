from django.db import models
import secrets

from branch.models import Branch
from Role.models import Role


def generate_token_key():
    return secrets.token_hex(20)


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)

    role = models.ForeignKey(
        Role,
        related_name="users",
        on_delete=models.CASCADE
    )

    branch = models.ForeignKey(
        Branch,
        related_name="users",
        on_delete=models.CASCADE
    )

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=20)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.username


class UserToken(models.Model):
    key = models.CharField(max_length=40, unique=True, default=generate_token_key)
    user = models.OneToOneField(
        User,
        related_name="auth_token",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
