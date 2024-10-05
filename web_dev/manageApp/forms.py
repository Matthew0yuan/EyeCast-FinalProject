from django import forms
from .models import Reservation,devices,ReservationData

class deviceForm(forms.ModelForm):
    class Meta:
        model = devices
        fields = ['serial_number', 'name', 'on_loan', 'holder', 'expected_return_date']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'vip_number', 'doctor_name', 'loan_length', 'earliest_start_date', 'contact_detail']

class UploadForm(forms.Form):
        file = forms.FileField()
        #model = ReservationData
        #fields = ['serial_number','vip_number','name','capture_date','capture_time','IOP_OD_left','IOP_OS_right','position']

        