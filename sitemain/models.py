from django.db import models
from django.contrib.auth.models import User

# Create your models here.

VEHICLE_TYPE = [
    ('Economy', 'ECONOMY'),
    ('Standard', 'STANDARD'),
    ('SUV', 'PREMIUM SUV'),
    ('Signature Series', 'SIGNATURE SERIES'),
]

RESERVATION_STATUS = [('Open', 'Open'), ('Paid', 'Paid'),
                      ('Close', 'Close'), ('Canceled', 'Canceled')]


class DealerLocation(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.location


class Vehicle(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=VEHICLE_TYPE, null=True)
    rate = models.IntegerField()
    licensenm = models.CharField(max_length=100)
    available_at = models.ForeignKey(
        DealerLocation, on_delete=models.CASCADE)

    def __str__(self):
        return self.model


class Reservation(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    pickup_date = models.DateField()
    return_date = models.DateField()
    pickup_location = models.ForeignKey(
        DealerLocation, on_delete=models.CASCADE, null=True, related_name='vehicle_pickup_location')
    return_location = models.ForeignKey(
        DealerLocation, on_delete=models.CASCADE, null=True, related_name='vehicle_return_location')
    type = models.CharField(max_length=100, choices=VEHICLE_TYPE, null=True)
    days_rented = models.IntegerField(null=True)
    order_total = models.IntegerField(null=True)
    reservation_status = models.CharField(
        max_length=100, default='Open', choices=RESERVATION_STATUS)

    def __str__(self):
        return str(self.customer)
