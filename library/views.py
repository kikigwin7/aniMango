from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Series, Item

# Create your views here.

def index(request):
    template = 'library/index.html'
    series_list = Series.objects.order_by('name')
    context = {
        'series_list': series_list
    }
    return render(request, template, context)

def series_view(request, series_id, media_type):
    template = 'library/view.html'
    library_series = get_object_or_404(
        Series,
        api_id=series_id,
        media_type=media_type
    )
    library_items = Item.objects.filter(parent_series=library_series)

    context = {
        'series': library_series,
        'items': library_items
    }
    return render(request, template, context)