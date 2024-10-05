from django.urls import path
from . import views

urlpatterns = [
    # path('', views.item_list, name='item_list'),
    # path('holder/<str:name>/', views.holder_detail, name='holder_detail'),
    path('', views.home, name='home'),
    path('adding_devices',views.add_device, name='add_device'),
    path('add_reservation',views.add_reservation, name='add_reservation'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('delete_device/<int:device_id>/', views.delete_device, name='delete_device'),
    path('device/edit/<int:device_id>/', views.edit_device, name='edit_device'),
    path('reservation/edit/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('devices/delete_selected/', views.delete_selected_reservation, name='delete_selected_reservation'),
    path('reservations/detail/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('upload_csv',views.upload_csv,name='upload_csv'),
]
