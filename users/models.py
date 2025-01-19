from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import normalize_newlines

from courses.models import Lesson, Course


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

class Payment(models.Model):

    CASH = 'cash'
    TRANSACTION= 'transaction'

    METHOD_CHOICES = [
        (CASH, 'Cash'),
        (TRANSACTION, 'Transaction'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='User')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='payments',
                               verbose_name='Course')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name='payments',
                               verbose_name='Lesson')
    date_of_payment = models.DateField(verbose_name='Date')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, verbose_name='Payment Method', default=CASH)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-date_of_payment']


    def __str__(self):
        return f'{self.user} - {self.lesson} - {self.date_of_payment} - {self.get_method_display()}'



