from django.db import models

class devices(models.Model):
    serial_number = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    on_loan = models.BooleanField(default=False)
    holder = models.CharField(max_length=100)
    expected_return_date = models.DateField()

    def __str__(self):
        return self.name
