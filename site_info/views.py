from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from news.models import Article
from .models import Exec, HistoryEntry


def home(request):
    news_l = Article.objects.order_by('-created')[:3]
    # Takes events that are in future, orders soonest first, takes first 4, then reverses (latest first) -Sorc
    events_l = Event.objects.filter(when__gte=timezone.now()).order_by('when')[:4]
    context = {
        'news_l': news_l,
        'events_l': events_l
    }
    return render(request, 'site_info/home.html', context)


def ssl(request):
    return render(request, 'site_info/ssl.html')

def constitution(request):
    return render(request, 'site_info/constitution.html')


def gdpr(request):
    return render(request, 'site_info/gdpr.html')


def contact(request):
    return render(request, 'site_info/contact.html')


def about(request):
    return render(request, 'site_info/about.html')


def exec_people(request, year):
    year_choices = Exec.objects.values('academic_year').distinct().order_by('-academic_year')
    exec_members = Exec.objects.filter(academic_year=year).order_by('place_in_list');
    context = {
        'disp_year': year,
        'year_choices': year_choices,
        'exec_members': exec_members
    }
    return render(request, 'site_info/exec.html', context)


def history(request):
    entries = HistoryEntry.objects.order_by('academic_year')
    context = {
        'history_list': entries
    }
    return render(request, 'site_info/history.html', context)
