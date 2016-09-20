from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse


def home(request):
	template = 'home/home.html'
	try:
		print(request.user.member.nick_or_name())
	except:
		print('Anonymous user')
	return render(request, template)