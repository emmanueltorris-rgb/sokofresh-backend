from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'ADMIN'
    FARMER = 'FARMER'
    BUYER = 'BUYER'
    OPERATOR = 'OPERATOR'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (FARMER, 'Farmer'),
        (BUYER, 'Buyer'),
        (OPERATOR, 'Operator'),
    ]

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=BUYER)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
