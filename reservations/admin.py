from django.contrib import admin
from .models import Room, Reservation, ReservationStatus, Guest, Service

admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(ReservationStatus)
admin.site.register(Guest)
admin.site.register(Service)
