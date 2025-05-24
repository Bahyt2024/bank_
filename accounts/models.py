from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    role = models.CharField(max_length=10, choices=[('client', 'Client'), ('admin', 'Admin')], default='client')
    is_activated = models.BooleanField(default=False)
    activation_link = models.CharField(max_length=255, blank=True, null=True)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
