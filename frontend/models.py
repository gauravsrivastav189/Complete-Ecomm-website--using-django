from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField

from django.contrib.auth.models import User

from mainapp import settings

CATEGORY_CHOICES = (
    ('C', 'Computer'),
    ('M', 'Mobile'),
    ('T', 'Tablet')
)

LABEL_CHOICES = (
    ('N', 'New'),
    ('R', 'Refurbished'),
    ('U', 'Used')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    label = models.CharField(choices=LABEL_CHOICES, max_length=5)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_discount_percent(self):
        discount_percent = 100 - ( self.discount_price * 100 / self.price)
        return discount_percent

    def get_item_url(self):
        return reverse('frontend:detail', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart(self):
        return reverse('frontend:add-to-cart', kwargs={
            'slug': self.slug
        })

    def snip_description(self):
        return self.description[:30] + "..."


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} - {self.item.title}"

    def total_item_price(self):
        return self.quantity * self.item.price

    def total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def amount_saved(self):
        return self.total_item_price() - self.total_discount_item_price()

    def final_price(self):
        if self.item.discount_price:
            return self.total_discount_item_price()
        return self.total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_ref = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)
    country = CountryField(max_length=100)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"