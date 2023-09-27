from django.contrib.auth.models import AbstractUser
from django.db import models

from mailing.models import NULLABLE


class Country(models.Model):
    country = models.CharField(max_length=40, verbose_name='страна')
    description = models.TextField(max_length=200, verbose_name='описание')
    flag = models.ImageField(upload_to='users/country/', verbose_name='превью', **NULLABLE)

    def __str__(self):
        return f'{self.country}'

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    patronymic = models.CharField(max_length=35, verbose_name='отчество', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='страна')
    verification_code = models.IntegerField(verbose_name='Код верификации', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


