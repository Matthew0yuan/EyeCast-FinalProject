# myapp/management/commands/import_products.py
from django.core.management.base import BaseCommand
import csv
from manageApp.models import ReservationData
from datetime import datetime  # Ensure correct import
with open('web_dev/rawdata.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Parse the date string into a datetime object
        capture_date = datetime.strptime(row['Date'], '%d/%m/%Y').date()
        # Parse the time string into a time object, if necessary
        capture_time = datetime.strptime(row['Time'], '%H:%M:%S').time()
        left = row['OD'] if row['OD'].strip() else None
        right = row['OS'] if row['OS'].strip() else None
    
        ReservationData.objects.create(
            capture_date=capture_date,
            capture_time=capture_time,
            vip_number=row['Patient ID'],
            IOP_OD_left=left,
            IOP_OS_right=right,
            position=row['Position'],
        )

