from django.db import models
from django.conf import settings


class Produce(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available_kg = models.IntegerField(default=0)
    image_url = models.URLField(blank=True)
    grade = models.CharField(max_length=50, default='Standard')
    is_active = models.BooleanField(default=True)
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='produce')
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_number
