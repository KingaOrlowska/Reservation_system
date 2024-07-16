from django import forms
from .models import Reservation, Room, Service


class ReservationForm(forms.ModelForm):
    guest_name = forms.CharField(label='Imię', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    guest_surname = forms.CharField(label='Nazwisko', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    guest_email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    guest_phone = forms.CharField(label='Telefon', max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    check_in = forms.DateField(label='Data zameldowania', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    check_out = forms.DateField(label='Data wymeldowania', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    guest_count = forms.IntegerField(label='Liczba osób', min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    rooms = forms.ModelMultipleChoiceField(
        queryset=Room.objects.all(),
        label='Pokoje',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
    )
    payment_method = forms.ChoiceField(choices=[('cash', 'Gotówka'), ('credit_card', 'Karta Kredytowa'), ('paypal', 'PayPal'), ('debit_card', 'Karta Debetowa')], label='Sposób płatności', widget=forms.Select(attrs={'class': 'form-control'}))
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        label='Usługi',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'})
    )

    class Meta:
        model = Reservation
        fields = ['guest_name', 'guest_surname', 'guest_email', 'guest_phone', 'check_in', 'check_out', 'guest_count', 'rooms', 'payment_method', 'services']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rooms'].queryset = Room.objects.all()
        self.fields['rooms'].label_from_instance = lambda obj: f"Pokój {obj.number} ({obj.get_type_display()})"
        self.fields['services'].queryset = Service.objects.all()
        self.fields['services'].label_from_instance = lambda obj: f"{obj.get_name_display()} - {obj.price} PLN"
