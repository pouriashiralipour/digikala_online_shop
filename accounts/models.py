from django.contrib.auth.models import AbstractUser
from django.db import models

from .custom_user_manager import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=11, unique=True)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_datetime_created = models.DateTimeField(auto_now=True)

    objects = CustomUserManager

    USERNAME_FIELD = "phone_number"

    REQUIRED_FIELDS = []
