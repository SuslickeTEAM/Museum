from django.shortcuts import render

from .models import Exhibit, Category, Event


# Exhibit view with prefetching related category to reduce database hits
def exhibits(request, pk):
    exhibits = Exhibit.objects.filter(category=pk).select_related('category')
    return render(request, 'exhibitions.html', {'exhibits': exhibits})


# Main view optimized with prefetch_related for better efficiency
def main(request):
    categories = Category.objects.prefetch_related('exhibit_set')  # prefetching related exhibits to reduce DB hits
    events = Event.objects.all()  # No need for prefetching in this case unless Events have relations
    return render(request, 'main.html', {'events': events, 'categories': categories})
