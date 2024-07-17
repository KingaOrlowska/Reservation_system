from django.contrib import admin
from django.urls import path
from reservations.views import (
    AdminDashboardView, ReceptionDashboardView, AddReservationView,
    EditReservationView, CalendarView, HotelStatisticsView, LoginView,
    DashboardView, LogoutView
)
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # Panel administracyjny Django
    path('login/', LoginView.as_view(), name='login'),  # Widok logowania
    path('logout/', LogoutView.as_view(), name='logout'),  # Widok wylogowania
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Widok główny dashboardu, przekierowuje w zależności od typu użytkownika
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),  # Widok dashboardu admina
    path('reception_dashboard/', ReceptionDashboardView.as_view(), name='reception_dashboard'),  # Widok dashboardu recepcji
    path('add_reservation/', AddReservationView.as_view(), name='add_reservation'),  # Widok do dodawania rezerwacji
    path('edit_reservation/<int:reservation_id>/', EditReservationView.as_view(), name='edit_reservation'),  # Widok do edycji rezerwacji
    path('calendar/', CalendarView.as_view(), name='calendar_view'),  # Widok kalendarza rezerwacji
    path('hotel_statistics/', HotelStatisticsView.as_view(), name='hotel_statistics'),  # Widok statystyk hotelu
    path('', RedirectView.as_view(url='login/', permanent=True)),  # Przekierowanie pustej ścieżki na stronę logowania
]
