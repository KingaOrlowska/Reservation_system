from datetime import date, timedelta, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from .models import Reservation, Room, Service, ReservationStatus, Guest
from .forms import ReservationForm

# Mixin wymagający uprawnień administratora
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('login')

# Mixin wymagający uprawnień recepcjonisty
class ReceptionRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.username == 'reception'

    def handle_no_permission(self):
        return redirect('login')

# Mixin dla obsługi CSRF
class CsrfExemptMixin:
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# Widok logowania z obsługą CSRF
class LoginView(CsrfExemptMixin, View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    def get(self, request):
        return render(request, 'login.html')

# Widok wylogowania
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')

# Widok główny, przekierowujący użytkowników na odpowiednie dashboardy
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.username == 'reception':
            return redirect('reception_dashboard')
        else:
            return redirect('login')

# Widok dashboardu admina
class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request):
        tiles = [
            {'title': 'Kalendarz', 'url': 'calendar_view'},
            {'title': 'Dodaj rezerwację', 'url': 'add_reservation'},
            {'title': 'Statystyki hotelu', 'url': 'hotel_statistics'},
        ]
        return render(request, 'admin_dashboard.html', {'tiles': tiles})

# Widok dashboardu recepcji
class ReceptionDashboardView(LoginRequiredMixin, ReceptionRequiredMixin, View):
    def get(self, request):
        tiles = [
            {'title': 'Kalendarz', 'url': 'calendar_view'},
            {'title': 'Dodaj rezerwację', 'url': 'add_reservation'},
            {'title': 'Statystyki hotelu', 'url': '#'},  # Link nieaktywny
        ]
        return render(request, 'reception_dashboard.html', {'tiles': tiles})

# Widok dodawania rezerwacji
class AddReservationView(LoginRequiredMixin, View):
    def get(self, request):
        check_in_date = request.GET.get('check_in')
        check_out_date = request.GET.get('check_out')

        available_rooms = Room.objects.all()
        if check_in_date and check_out_date:
            try:
                check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
                reserved_rooms = Reservation.objects.filter(
                    check_in__lt=check_out_date,
                    check_out__gt=check_in_date
                ).values_list('rooms', flat=True)
                available_rooms = available_rooms.exclude(id__in=reserved_rooms)
            except ValueError:
                messages.error(request, "Enter a valid date.")

        form = ReservationForm(initial={'check_in': check_in_date, 'check_out': check_out_date})
        return render(request, 'add_reservation.html', {'form': form, 'available_rooms': available_rooms})

    def post(self, request):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            # Utworzenie statusu rezerwacji
            ReservationStatus.objects.create(reservation=reservation, status='Nowa')

            # Utworzenie lub przypisanie gościa do rezerwacji
            guest, created = Guest.objects.get_or_create(user=request.user)
            guest.reservations.add(reservation)

            # Wysyłanie e-maila
            send_mail(
                'Potwierdzenie rezerwacji',
                f'Twoja rezerwacja została dokonana na termin od {reservation.check_in} do {reservation.check_out}.',
                'your_email@example.com',
                [reservation.guest_email],
                fail_silently=False,
            )

            return redirect(reverse('calendar_view'))

        # Jeśli formularz nie jest poprawny, ponownie pobieramy dostępne pokoje
        check_in_date = request.POST.get('check_in')
        check_out_date = request.POST.get('check_out')
        available_rooms = Room.objects.all()

        if check_in_date and check_out_date:
            try:
                check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
                reserved_rooms = Reservation.objects.filter(
                    check_in__lt=check_out_date,
                    check_out__gt=check_in_date
                ).values_list('rooms', flat=True)
                available_rooms = available_rooms.exclude(id__in=reserved_rooms)
            except ValueError:
                messages.error(request, "Enter a valid date.")

        return render(request, 'add_reservation.html', {'form': form, 'available_rooms': available_rooms})

# Widok edycji rezerwacji
class EditReservationView(LoginRequiredMixin, View):
    def get(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        form = ReservationForm(instance=reservation)

        # Pobierz zarezerwowane pokoje
        reserved_rooms = reservation.rooms.all()

        # Pobierz dodatkowe pokoje, które nie są zarezerwowane w danym terminie
        check_in_date = reservation.check_in
        check_out_date = reservation.check_out
        all_rooms = Room.objects.all()
        reserved_rooms_ids = reserved_rooms.values_list('id', flat=True)
        available_rooms = all_rooms.exclude(id__in=reserved_rooms_ids)

        return render(request, 'edit_reservation.html', {
            'form': form,
            'reserved_rooms': reserved_rooms,
            'available_rooms': available_rooms,
            'reserved_services': reservation.services.all()  # Nowe pole dla usług
        })

    def post(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if 'delete' in request.POST:
            reservation.delete()
            send_mail(
                'Anulacja rezerwacji',
                f'Twoja rezerwacja na termin od {reservation.check_in} do {reservation.check_out} została anulowana.',
                'your_email@example.com',
                [reservation.guest_email],
                fail_silently=False,
            )
            return redirect(reverse('calendar_view'))
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save()
            send_mail(
                'Aktualizacja rezerwacji',
                f'Twoja rezerwacja została zaktualizowana na termin od {reservation.check_in} do {reservation.check_out}.',
                'your_email@example.com',
                [reservation.guest_email],
                fail_silently=False,
            )

            return redirect(reverse('calendar_view'))

        # Jeśli formularz nie jest poprawny, ponownie pobieramy dostępne pokoje
        check_in_date = reservation.check_in
        check_out_date = reservation.check_out
        available_rooms = Room.objects.all()

        reserved_rooms = Reservation.objects.filter(
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        ).exclude(id=reservation_id).values_list('rooms', flat=True)
        available_rooms = available_rooms.exclude(id__in=reserved_rooms)

        return render(request, 'edit_reservation.html', {
            'form': form,
            'available_rooms': available_rooms,
            'reserved_services': reservation.services.all()  # Nowe pole dla usług
        })

# Widok kalendarza rezerwacji
class CalendarView(LoginRequiredMixin, View):
    def get(self, request):
        # Pobierz wszystkie rezerwacje
        reservations = Reservation.objects.all()

        # Przygotuj dane do wyświetlenia w kalendarzu
        events = [
            {
                'title': f"{reservation.guest_name} {reservation.guest_surname}",
                'start': reservation.check_in.isoformat(),
                'end': (reservation.check_out + timedelta(days=1)).isoformat(),  # FullCalendar expects end date to be exclusive
                'description': f"Pokój: {room.number} ({room.get_type_display()}), Liczba gości: {reservation.guest_count}",
                'url': reverse('edit_reservation', args=[reservation.id])
            }
            for reservation in reservations
            for room in reservation.rooms.all()
        ]

        # Pobierz numery pokoi
        rooms = Room.objects.all().order_by('number')

        # Sprawdź liczbę zarezerwowanych pokoi na dany dzień
        daily_room_reservations = {}
        for reservation in reservations:
            for day in range((reservation.check_out - reservation.check_in).days + 1):
                current_day = reservation.check_in + timedelta(days=day)
                daily_room_reservations[current_day] = daily_room_reservations.get(current_day, 0) + reservation.rooms.count()

        # Dodaj komunikat o przekroczeniu liczby zarezerwowanych pokoi
        for day, count in daily_room_reservations.items():
            if count > 10:  # Próg 10 pokoi
                request.session.setdefault('messages', [])
                request.session['messages'].append(f"Sprawdź stan magazynowy hotelu, liczba zarezerwowanych pokoi na dzień {day} przekroczyła 10.")

        messages_from_session = request.session.get('messages', [])
        for msg in messages_from_session:
            messages.warning(request, msg)

        context = {
            'events': events,
            'rooms': rooms,
            'current_date': timezone.now().date(),
            'days': [date.today() + timedelta(days=i) for i in range(30)]  # przykład następnych 30 dni
        }
        return render(request, 'calendar.html', context)

    def post(self, request):
        if 'clear_messages' in request.POST:
            request.session['messages'] = []
        return redirect(reverse('calendar_view'))

# Widok statystyk hotelu
class HotelStatisticsView(LoginRequiredMixin, View):
    def get(self, request):
        # Pobierz wszystkie rezerwacje z obecnego i poprzedniego roku
        current_year = datetime.now().year
        previous_year = current_year - 1

        reservations = Reservation.objects.all()
        current_year_reservations = reservations.filter(check_in__year=current_year)
        previous_year_reservations = reservations.filter(check_in__year=previous_year)

        # Inicjalizacja statystyk miesięcznych
        monthly_stats = {
            'current_year': {month: 0 for month in range(1, 13)},
            'previous_year': {month: 0 for month in range(1, 13)}
        }
        monthly_guest_counts = {month: 0 for month in range(1, 13)}
        monthly_revenue = {month: 0 for month in range(1, 13)}
        payment_methods = {'cash': 0, 'credit_card': 0, 'paypal': 0, 'debit_card': 0}
        room_stats = {room.number: 0 for room in Room.objects.all()}
        service_stats = {service.name: 0 for service in Service.objects.all()}

        # Zbieranie danych
        for reservation in current_year_reservations:
            month = reservation.check_in.month
            monthly_stats['current_year'][month] += 1
            monthly_guest_counts[month] += reservation.guest_count
            monthly_revenue[month] += reservation.rooms.count() * 100  # Przykładowa cena pokoju
            payment_methods[reservation.payment_method] += 1
            for room in reservation.rooms.all():
                room_stats[room.number] += 1
            for service in reservation.services.all():
                service_stats[service.name] += 1

        for reservation in previous_year_reservations:
            month = reservation.check_in.month
            monthly_stats['previous_year'][month] += 1

        context = {
            'monthly_stats': monthly_stats,
            'monthly_guest_counts': monthly_guest_counts,
            'monthly_revenue': monthly_revenue,
            'payment_methods': payment_methods,
            'room_stats': room_stats,
            'service_stats': service_stats,
        }

        return render(request, 'hotel_statistics.html', context)
