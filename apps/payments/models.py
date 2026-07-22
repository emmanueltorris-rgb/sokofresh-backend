from django.db import models
from django.conf import settings

class MpesaTransaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey('marketplace.Order', on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey('cold_storage.ColdStorageBooking', on_delete=models.CASCADE, null=True, blank=True)
    
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    result_code = models.CharField(max_length=10, blank=True)
    result_desc = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True)
    transaction_date = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)