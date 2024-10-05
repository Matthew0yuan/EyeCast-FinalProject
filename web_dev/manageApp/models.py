from django.db import models

# Create your models here.
class devices(models.Model):
    serial_number = models.CharField(max_length=50)#pk
    name = models.CharField(max_length=100)
    on_loan = models.BooleanField(default=False)
    holder = models.CharField(max_length=100)
    expected_return_date = models.DateField()

    def __str__(self):
        return self.name
    
class Reservation(models.Model):
    name = models.CharField(max_length=100)
    vip_number = models.CharField(max_length=50)#pk
    doctor_name = models.CharField(max_length=100)
    loan_length = models.IntegerField(help_text="Duration in days")
    earliest_start_date = models.DateField()
    contact_detail = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.vip_number})"
    
# models.py

class ReservationData(models.Model):
    serial_number = models.CharField(null=True, blank=True,max_length=50)  # fk
    vip_number = models.CharField(max_length=50)  # fk
    name = models.CharField(max_length=100)  # Added name field
    capture_date = models.DateField()  # pk
    capture_time = models.TimeField()  # pk
    IOP_OD_left = models.IntegerField(null=True, blank=True)
    IOP_OS_right = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=15)
    

    def __str__(self):
        return f"{self.name} ({self.vip_number})"
