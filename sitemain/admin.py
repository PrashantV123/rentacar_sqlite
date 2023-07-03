from django.contrib import admin
from .models import Vehicle, Reservation, DealerLocation


# Register your models here.

@admin.register(DealerLocation)
class DealerLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'location']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'model', 'type',
                    'rate', 'licensenm',  'available_at',
                    ]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'vehicle', 'type', 'pickup_date', 'return_date', 'pickup_location', 'return_location', 'days_rented', 'order_total', 'reservation_status',
                    ]
