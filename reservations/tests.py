import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from reservations.models import Room, Service, Reservation, ReservationStatus, Guest

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(username='admin', password='admin')

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(username='adminuser', password='password', email='admin@example.com')

@pytest.fixture
def room():
    return Room.objects.create(type='single', number=101)

@pytest.fixture
def service():
    return Service.objects.create(name='spa', price=200.00)

@pytest.fixture
def reservation(user, room, service):
    reservation = Reservation.objects.create(
        guest_name='John',
        guest_surname='Doe',
        guest_email='john.doe@example.com',
        guest_phone='123456789',
        guest_count=2,
        check_in='2024-07-20',
        check_out='2024-07-25',
        payment_method='cash',
    )
    reservation.rooms.add(room)
    reservation.services.add(service)
    return reservation

@pytest.mark.django_db
def test_login_view(client, user):
    url = reverse('login')
    response = client.post(url, {'username': 'reception', 'password': 'reception'})
    assert response.status_code == 302  # Redirects to dashboard
    assert response.url == reverse('dashboard')

@pytest.mark.django_db
def test_admin_dashboard_view(client, admin_user):
    client.login(username='adminuser', password='password')
    url = reverse('admin_dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Admin Dashboard' in response.content.decode()

@pytest.mark.django_db
def test_reception_dashboard_view(client, user):
    client.login(username='testuser', password='password')
    user.username = 'reception'
    user.save()
    url = reverse('reception_dashboard')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Reception Dashboard' in response.content.decode()

@pytest.mark.django_db
def test_add_reservation_view(client, user, room, service):
    client.login(username='testuser', password='password')
    url = reverse('add_reservation')
    response = client.get(url)
    assert response.status_code == 200

    form_data = {
        'guest_name': 'Jane',
        'guest_surname': 'Doe',
        'guest_email': 'jane.doe@example.com',
        'guest_phone': '987654321',
        'guest_count': 1,
        'check_in': '2024-07-20',
        'check_out': '2024-07-22',
        'payment_method': 'cash',
        'rooms': [room.id],
        'services': [service.id],
    }
    response = client.post(url, form_data)
    assert response.status_code == 302  # Redirects to calendar view
    assert Reservation.objects.filter(guest_name='Jane').exists()

@pytest.mark.django_db
def test_edit_reservation_view(client, user, reservation, room, service):
    client.login(username='testuser', password='password')
    url = reverse('edit_reservation', args=[reservation.id])
    response = client.get(url)
    assert response.status_code == 200

    form_data = {
        'guest_name': 'John',
        'guest_surname': 'Doe',
        'guest_email': 'john.doe@example.com',
        'guest_phone': '123456789',
        'guest_count': 2,
        'check_in': '2024-07-21',  # Updated check-in date
        'check_out': '2024-07-25',
        'payment_method': 'cash',
        'rooms': [room.id],
        'services': [service.id],
    }
    response = client.post(url, form_data)
    assert response.status_code == 302  # Redirects to calendar view
    reservation.refresh_from_db()
    assert reservation.check_in.strftime('%Y-%m-%d') == '2024-07-21'
