from django.db import models


class UserModel(models.Model):
    username = models.CharField(max_length=100, verbose_name="Имя", unique=True)
    balance = models.PositiveIntegerField(default=0, verbose_name="Баланс")
