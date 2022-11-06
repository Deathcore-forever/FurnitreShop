from django.db import models
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.models import User


class Basket(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)


class Maker(models.Model):
    name_maker = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=11, default="")


class Furniture(models.Model):
    name_fur = models.CharField(max_length=100, default="")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True, default="")
    on_storage = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE, blank=False)
    color = models.CharField(max_length=50, default="")
    weight = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'мебель'
        verbose_name_plural = 'мебель'


class BasketContent(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, blank=False)
    fur = models.ForeignKey(Furniture, on_delete=models.CASCADE, blank=False)
    quantity = models.IntegerField(default=0)


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, blank=False)
    order_date = models.DateTimeField(auto_now=True)
    order_address = models.CharField(max_length=100, default='')
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    paid_for = models.IntegerField()
