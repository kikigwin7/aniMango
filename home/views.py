from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse


def home(request):
	template = 'home/home.html'
	return render(request, template)

def login_view(request):
	template = 'home/login.html'
	if request.method == 'POST':
		uname = request.POST['username']
		pwd = request.POST['password']
		user = authenticate(username=uname, password=pwd)
		if user is not None:
			if user.is_active:
				login(request, user)
				messages.success(request, 'You have been logged in')
				return HttpResponseRedirect(reverse('home'))
			else:
				messages.error(request, 'Your account has been disabled')
				return render(request, template)
		else:
			# Incorrect password or username as authenticate returned None
			messages.error(request, 'Username or password incorrect')
			return render(request, template)
	else:
		return render(request, template)

def logout_view(request):
	logout(request)
	messages.success(request, 'User logged out')
	return HttpResponseRedirect(reverse('home'))