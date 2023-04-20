import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(default=None)

    def __str__(self):
        return str(self.name)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return ''


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    
    def get_cart_items(self):
        item_sum = 0
        for orderitem in self.orderitem_set.all():
            item_sum += orderitem.quantity
        return item_sum
    
    def get_cart_subtotal(self):
        subtotal = 0
        for orderitem in self.orderitem_set.all():
            item_total = float(orderitem.get_item_total())
            subtotal += item_total
        return subtotal
    
    def calculate_tax(self, subtotal):
        tax = 0.075 * subtotal
        return tax
    
    def get_cart_grandtotal(self):
        subtotal = self.get_cart_subtotal()
        tax = self.calculate_tax(subtotal)
        grandtotal = subtotal + tax
        return grandtotal
    
    def __str__(self):
        return "Order " + str(self.pk)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)

    def get_item_total(self):
        item_total = self.quantity * self.product.price
        return item_total
    
    def __str__(self):
        return self.product.name


class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

