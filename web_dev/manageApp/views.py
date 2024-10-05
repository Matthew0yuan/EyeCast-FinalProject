from django.shortcuts import render, redirect
from .models import devices, Reservation, ReservationData
from .forms import ReservationForm, deviceForm,UploadForm
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime,timedelta
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Create your views here.
#contains a main page, with two tables create/delete/search
#creating new device  / deleting device
#check in device / check out device
#allow user to click into the name, and select show the reading from the patient

def home(request):
    Devices = devices.objects.all()
    Reservations = Reservation.objects.all()
    return render(request, 'manageApp/home.html', {
        'devices': Devices,
        'reservations': Reservations
    })

def add_device(request):
    if request.method == 'POST':
        form = deviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the same page to prevent double submissions
    else:
        form = deviceForm()  # Create an empty form for GET request
    Devices = devices.objects.all()
    return render(request, 'manageApp/add_device.html', {
        'form': form,
        #'items': Devices,
    })

def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the same page to prevent double submissions
    else:
        form = ReservationForm()  # Create an empty form for GET request
        #reservations = Reservation.objects.all()
    return render(request, 'manageApp/add_reservation.html', {
        'form': form,
        #'reservations': reservations
    })

#deleting function
def delete_reservation(request, reservation_id):#keep on working on deleting selecting button
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('home')  # Redirect back to the home page after deletion

def delete_device(request, device_id):
    device = get_object_or_404(devices, id=device_id)  # Assuming your model is named `devices`, consider renaming it to `Device` for convention
    device.delete()
    return redirect('home')

@require_POST
def delete_selected_reservation(request):
    selected_ids = request.POST.getlist('selected_reservation')
    if selected_ids:
        Reservation.objects.filter(id__in=selected_ids).delete()
    return redirect('home') 

#editing function
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'manageApp/edit_reservation.html', {'form': form, 'reservation_id': reservation.id})

def edit_device(request, device_id):
    device = get_object_or_404(devices, id=device_id)
    if request.method == 'POST':
        form = deviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = deviceForm(instance=device)
    return render(request, 'manageApp/edit_device.html', {'form': form, 'device_id': device.id})

def upload_csv(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
#edit this part for taking into the data correctly
            for row in reader:
                #print(row)
                ReservationData.objects.create(
                    # serial_number=row['serial_number'],
                    vip_number=row['Patient ID'],
                    # name=row['name'],
                    capture_date=datetime.strptime(row['Date'], '%d/%m/%Y').date(),
                    capture_time=datetime.strptime(row['Time'], '%H:%M:%S').time(),
                    IOP_OD_left=row['OD'] or None,
                    IOP_OS_right=row['OS'] or None,
                    position=row['Position']
                )
            return redirect('home')  # Redirect after POST
    else:
        form = UploadForm()
    return render(request, 'manageApp/upload_csv.html', {'form': form})


def reservation_detail(request, reservation_id):
    print(reservation_id)
    data = ReservationData.objects.filter(vip_number=reservation_id)
    # if not data.exists():
    #     return render(request, 'patient_not_found.html', {'vip_number': reservation_id})

    # Convert QuerySet to DataFrame
    df = pd.DataFrame(list(data.values()))
    print(data)

    print(df)
    print(df.columns)
    # df['capture_date'] = pd.to_datetime(df['capture_date'], format='%d/%m/%Y')
    df['capture_time'] = pd.to_datetime(df['capture_time'], format='%H:%M:%S')
    print(df['capture_time'])
    #df['datetime'] = pd.to_datetime(df['capture_date'] + ' ' + df['capture_time'], format='%d/%m/%Y %H:%M:%S')
    #df['time_slot'] = (df['capture_time'].dt.hour // 2) * 2
    #df['time_slot'] = df['time_slot'].astype(str) + ":00"

    # Plotly figures

    fig_left_eye = px.scatter(
        df,
        x='capture_time',
        y='IOP_OD_left',
        title='IOP OD Left Over Time',
        labels={'capture_time': 'time', 'IOP_OD_left': 'IOP OD Left'},
        hover_data={'capture_date': True} 
    )

    # Example: Plot IOP_OD_right over time
    fig_right_eye = px.scatter(
        df,
        x='capture_time',
        y='IOP_OS_right',
        title='IOP OS Right Over Time',
        labels={'capture_time': 'Time', 'IOP_OS_right': 'IOP OS Right'},
        hover_data={'capture_date': True} 
    )
    
    df['datetime'] = pd.to_datetime(df['capture_date'].astype(str) + ' ' + df['capture_time'].astype(str))
    # Setting datetime as the index
    df.set_index('datetime', inplace=True)
    # Resample data into 2-hour bins for candlestick chart
    resampled = df['IOP_OD_left'].resample('2H').agg(['min', 'max', 'mean'])

    # Create a candlestick
    candlestick_fig = go.Figure(data=[go.Candlestick(#bug in here
        x=resampled.index,
        open=resampled['mean'],
        high=resampled['max'],
        low=resampled['min'],
        close=resampled['mean']
    )])

    # Update layout for the candlestick chart
    candlestick_fig.update_layout(
        title='IOP OD Left Readings Over Time',
        xaxis_title='Time',
        yaxis_title='IOP OD Left',
        xaxis_rangeslider_visible=False
    )

    # Convert figures to HTML
    graph_div_left = fig_left_eye.to_html(full_html=False)
    graph_div_right = fig_right_eye.to_html(full_html=False)
    graph_div_candlestick = candlestick_fig.to_html(full_html=False)
    # Render the template
    return render(request, 'manageApp/detail.html', {
        'graph_div_left': graph_div_left,
        'graph_div_right': graph_div_right,
        'graph_div_candlestick': graph_div_candlestick,
        'vip_number': reservation_id,
    })
