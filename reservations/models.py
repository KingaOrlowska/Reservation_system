from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]
    type = models.CharField(max_length=10, choices=ROOM_TYPES)
    number = models.IntegerField()

    def __str__(self):
        return f'Room {self.number} ({self.get_type_display()})'

class Service(models.Model):
    SERVICE_CHOICES = [
        ('none', 'Brak - 0 zł'),
        ('spa', 'Spa - 200 zł'),
        ('room_service', 'Room Service - 50 zł'),
        ('parking', 'Parking - 15 zł'),
        ('gastronomy', 'Gastronomia - 100 zł'),
    ]
    name = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.get_name_display()}'

class Reservation(models.Model):
    rooms = models.ManyToManyField(Room)
    guest_name = models.CharField(max_length=100)
    guest_surname = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=15, default='000000000')
    guest_count = models.IntegerField()
    check_in = models.DateField()
    check_out = models.DateField()
    payment_method = models.CharField(max_length=20, default='cash')
    services = models.ManyToManyField(Service)

    def __str__(self):
        return f'Reservation for {self.guest_name} {self.guest_surname} from {self.check_in} to {self.check_out}'

class ReservationStatus(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f'Status for {self.reservation}'

class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    reservations = models.ManyToManyField(Reservation, related_name='guests')

    def __str__(self):
        return f'Guest {self.user.username if self.user else self.id}'
