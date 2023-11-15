from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    name = models.CharField(max_length=50, verbose_name='имя', **NULLABLE)
    surname = models.CharField(max_length=50, verbose_name='фамилия', **NULLABLE)
    code = models.CharField(verbose_name='код', unique=True, **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активный')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [""]

    class Meta:
        permissions = [
            (
                "set_is_active",
                "can block users (is active)"
            ),
        ]
