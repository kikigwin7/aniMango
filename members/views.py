from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.core.urlresolvers import reverse
from library.models import Item

def profile(request):
	template = "members/profile.html"
	if request.user.is_authenticated():
		return render(request, template)
	else:
		messages.error(request, 'You must be logged in to view this page')
		return HttpResponseRedirect(reverse('home'))

def profile_edit(request):
	template = "members/edit.html"
	if not request.user.is_authenticated():
		messages.error(request, 'You must be logged in to edit your profile')
		return HttpResponseRedirect(reverse('member:profile'))

	if request.method == 'POST':
		user_prof = request.user.member
		user_prof.nick = request.POST['nick']
		user_prof.bio = request.POST['bio']
		user_prof.profile_url = request.POST['pic']
		user_prof.save()
		messages.success(request, 'Your profile was successfully updated')
		return HttpResponseRedirect(reverse('member:profile'))
	else:
		return render(request, template)

def login_view(request):
	template = 'members/login.html'
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
	messages.success(request, 'You have been logged out')
	return HttpResponseRedirect(reverse('home'))