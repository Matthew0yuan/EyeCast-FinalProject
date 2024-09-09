
from django.shortcuts import render

from .model import devices
def home(request):
    return render(request, 'home.html')
#NOTE when everytime you updating "views.py" the urls.py has to be updated as wells

def item_list(request):
    items = devices.objects.all()
    return render(request, 'borrow/item_list.html', {'items': items})

def holder_detail(request, name):
    items = devices.objects.filter(holder=name)
    return render(request, 'borrow/holder_detail.html', {'items': items, 'name': name})