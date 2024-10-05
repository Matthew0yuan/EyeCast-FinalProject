from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'vip_number', 'doctor_name', 'loan_length', 'earliest_start_date', 'contact_detail']
