from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import normalize_newlines


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Phone number')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='City')
    avatar = models.ImageField(upload_to='users/avatars', blank=True, null=True, verbose_name='Avatar')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return normalize_newlines(self.email)


