from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse
from news.models import Article


def home(request):
	template = 'home/home.html'
	news_l = Article.objects.order_by('-created')[:3]
	context = {
		'news_l': news_l,
	}
	return render(request, template, context)