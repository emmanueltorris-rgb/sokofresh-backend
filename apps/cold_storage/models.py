from django.db import models
from django.conf import settings


class ColdRoom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class ColdStorageBooking(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cold_room = models.ForeignKey(ColdRoom, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.cold_room.name}"
