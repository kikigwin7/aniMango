from django.shortcuts import render
from news.models import Article
from events.models import Event
from .models import HistoryEntry


def home(request):
	template = 'site_info/home.html'
	news_l = Article.objects.order_by('-created')[:3]
	events_l = Event.objects.order_by('-when')[:4]
	context = {
		'news_l': news_l,
		'events_l':events_l
	}
	return render(request, template, context)

def general(request):
	template = 'site_info/general_info.html'
	pass

def constitution(request):
	template = 'site_info/constitution.html'
	return render(request, template)

def exec_people(request):
	template = 'site_info/exec.html'
	pass

def history(request):
	template = 'site_info/history.html'
	entries = HistoryEntry.objects.order_by('academic_year')
	context = {
		'history_list': entries
	}
	return render(request, template, context)