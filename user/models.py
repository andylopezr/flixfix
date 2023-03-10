from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import EmailField, BooleanField
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Email as username field, uses the user manager"""
    email = EmailField(max_length=255, blank=False, unique=True)
    is_active = BooleanField(default=True)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
