from django.shortcuts import render
from .forms import ExhibitForm
from .models import *

def exhibits(request, pk):
    exhibits = Exhibit.objects.filter(pk=pk)
    return render(request, 'exhibitions.html', {'exhibits': exhibits})

def main(request):
    category = Category.objects.all()
    events = Event.objects.all()
    return render(request, 'main.html', {'events': events, 'categories': category})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
