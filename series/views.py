from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Series

# Create your views here.

def index(request):
    response = "This is the series index"
    return HttpResponse(response)

def series_view(request, series_id, media_type):
    template = 'series/view.html'
    series = get_object_or_404(Series, api_id=series_id, media_type=media_type)
    context = {
        'title': series.name,
        'cover_image': series.cover_link,
        'synopsis': series.synopsis,
        'anilist_link': series.ani_link
    }
    return render(request, template, context)