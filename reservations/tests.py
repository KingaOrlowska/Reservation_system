import pytest
from django.urls import reverse
from reservations.models import Room, Service, Reservation, ReservationStatus, Guest
from reservations.forms import ReservationForm

@pytest.mark.django_db
class TestLoginView:
    def test_login_get(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200
        assert 'login.html' in [t.name for t in response.templates]

    def test_login_post_valid(self, client, user):
        response = client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        assert response.status_code == 302
        assert response.url == reverse('dashboard')

@pytest.mark.django_db
class TestLogoutView:
    def test_logout(self, client, user):
        client.login(username='testuser', password='testpass')
        response = client.get(reverse('logout'))
        assert response.status_code == 302
        assert response.url == reverse('login')

    def test_logout_not_logged_in(self, client):
        response = client.get(reverse('logout'))
        assert response.status_code == 302
        assert response.url == f"{reverse('login')}?next=/logout/"

@pytest.mark.django_db
class TestDashboardView:
    def test_dashboard_admin(self, client, admin_user):
        client.login(username='admin', password='admin')
        response = client.get(reverse('dashboard'))
        assert response.status_code == 302
        assert response.url == reverse('admin_dashboard')

    def test_dashboard_reception(self, client, reception_user):
        client.login(username='reception', password='reception')
        response = client.get(reverse('dashboard'))
        assert response.status_code == 302
        assert response.url == reverse('reception_dashboard')

@pytest.mark.django_db
class TestAdminDashboardView:
    def test_admin_dashboard_access(self, client, admin_user):
        client.login(username='admin', password='admin')
        response = client.get(reverse('admin_dashboard'))
        assert response.status_code == 200
        assert 'admin_dashboard.html' in [t.name for t in response.templates]

    def test_admin_dashboard_no_access(self, client, user):
        client.login(username='testuser', password='testpass')
        response = client.get(reverse('admin_dashboard'))
        assert response.status_code == 302
        assert response.url == reverse('login')

@pytest.mark.django_db
class TestReceptionDashboardView:
    def test_reception_dashboard_access(self, client, reception_user):
        client.login(username='reception', password='reception')
        response = client.get(reverse('reception_dashboard'))
        assert response.status_code == 200
        assert 'reception_dashboard.html' in [t.name for t in response.templates]

    def test_reception_dashboard_no_access(self, client, user):
        client.login(username='testuser', password='testpass')
        response = client.get(reverse('reception_dashboard'))
        assert response.status_code == 302
        assert response.url == reverse('login')

@pytest.mark.django_db
class TestAddReservationView:
    def test_get_add_reservation(self, client, user):
        client.login(username='testuser', password='testpass')
        response = client.get(reverse('add_reservation'))
        assert response.status_code == 200
        assert 'add_reservation.html' in [t.name for t in response.templates]

    def test_post_add_reservation(self, client, user):
        client.login(username='testuser', password='testpass')
        room = Room.objects.create(type='single', number=101)
        data = {
            'guest_name': 'Jan',
            'guest_surname': 'Kowalski',
            'guest_email': 'jan.kowalski@example.com',
            'guest_phone': '123456789',
            'guest_count': 1,
            'check_in': '2023-12-01',
            'check_out': '2023-12-05',
            'payment_method': 'cash',
            'rooms': [room.id],
            'services': []
        }
        response = client.post(reverse('add_reservation'), data)
        if response.status_code != 302:
            print(response.content)
        assert response.status_code == 302
        assert response.url == reverse('calendar_view')

@pytest.mark.django_db
class TestEditReservationView:
    def test_get_edit_reservation(self, client, user):
        client.login(username='testuser', password='testpass')
        room = Room.objects.create(type='single', number=101)
        reservation = Reservation.objects.create(
            guest_name='Jan', guest_surname='Kowalski', guest_email='jan.kowalski@example.com',
            guest_phone='123456789', guest_count=1, check_in='2023-12-01',
            check_out='2023-12-05', payment_method='cash'
        )
        reservation.rooms.add(room)
        response = client.get(reverse('edit_reservation', args=[reservation.id]))
        assert response.status_code == 200
        assert 'edit_reservation.html' in [t.name for t in response.templates]

    def test_post_edit_reservation(self, client, user):
        client.login(username='testuser', password='testpass')
        room = Room.objects.create(type='single', number=101)
        reservation = Reservation.objects.create(
            guest_name='Jan', guest_surname='Kowalski', guest_email='jan.kowalski@example.com',
            guest_phone='123456789', guest_count=1, check_in='2023-12-01',
            check_out='2023-12-05', payment_method='cash'
        )
        reservation.rooms.add(room)
        data = {
            'guest_name': 'Anna',
            'guest_surname': 'Nowak',
            'guest_email': 'anna.nowak@example.com',
            'guest_phone': '987654321',
            'guest_count': 2,
            'check_in': '2023-12-02',
            'check_out': '2023-12-06',
            'payment_method': 'credit_card',
            'rooms': [room.id],
            'services': []
        }
        response = client.post(reverse('edit_reservation', args=[reservation.id]), data)
        if response.status_code != 302:
            print(response.content)
        assert response.status_code == 302
        assert response.url == reverse('calendar_view')

@pytest.mark.django_db
class TestCalendarView:
    def test_get_calendar_view(self, client, user):
        client.login(username='testuser', password='testpass')
        response = client.get(reverse('calendar_view'))
        assert response.status_code == 200
        assert 'calendar.html' in [t.name for t in response.templates]

    def test_post_calendar_clear_messages(self, client, user):
        client.login(username='testuser', password='testpass')
        session = client.session
        session['messages'] = ['Test message']
        session.save()
        response = client.post(reverse('calendar_view'), {'clear_messages': True})
        assert response.status_code == 302
        assert response.url == reverse('calendar_view')
        session = client.session
        session.load()  # Reload the session to reflect changes made by the view
        assert 'messages' not in session

@pytest.mark.django_db
class TestHotelStatisticsView:
    def test_get_hotel_statistics_view(self, client, user):
        client.login(username='testuser', password='testpass')
        response = client.get(reverse('hotel_statistics'))
        assert response.status_code == 200
        assert 'hotel_statistics.html' in [t.name for t in response.templates]

    def test_get_hotel_statistics_view_with_data(self, client, user):
        client.login(username='testuser', password='testpass')
        room = Room.objects.create(type='single', number=101)
        reservation = Reservation.objects.create(
            guest_name='Jan', guest_surname='Kowalski', guest_email='jan.kowalski@example.com',
            guest_phone='123456789', guest_count=1, check_in='2023-12-01',
            check_out='2023-12-05', payment_method='cash'
        )
        reservation.rooms.add(room)
        response = client.get(reverse('hotel_statistics'))
        assert response.status_code == 200
        assert 'hotel_statistics.html' in [t.name for t in response.templates]
        if b'Jan Kowalski' not in response.content:
            print(response.content)
        assert b'Jan Kowalski' in response.content
