from django.shortcuts import render
from news.models import Article
from events.models import Event


def home(request):
	template = 'home/home.html'
	news_l = Article.objects.order_by('-created')[:3]
	events_l = Event.objects.order_by('-when')[:4]
	context = {
		'news_l': news_l,
		'events_l':events_l
	}
	return render(request, template, context)