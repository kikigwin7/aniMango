from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse


def home(request):
	template = 'home/home.html'
	return render(request, template)