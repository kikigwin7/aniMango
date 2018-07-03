import os
from PIL import Image

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from library.models import ArchivedRequest, Request

@login_required
def profile(request):
	loaned_items = Request.objects.select_related().filter(user=request.user).order_by('-return_deadline')
	archived_items = ArchivedRequest.objects.select_related().filter(user=request.user).order_by('-date_requested')[:5]
	context = {
		'loaned_items': loaned_items,
		'archived_items': archived_items
	}
	return render(request, 'members/profile.html', context)

@login_required
def view(request, user_id):
	context = { 'other_user': get_object_or_404(User, id=user_id) }
	return render(request, "members/other_profile.html", context)

@login_required
def profile_edit(request):
	if request.method == 'POST':
		user_prof = request.user.member
		user_prof.nick = request.POST.get('nick')
		user_prof.bio = request.POST.get('bio')
		user_prof.discordTag = request.POST.get('discordTag')
		user_prof.show_full_name = True if request.POST.get('show_name') else False
		if request.FILES:
			try:
				# Throws exception if file is not an image
				im = Image.open(request.FILES['img'])
				name, ext = os.path.splitext(request.FILES['img'].name)
				if ext not in ['.jpg', '.jpeg', '.png']:
					raise Warning('Wrong image format')
				user_prof.img = request.FILES['img']
			except:
				messages.error(request, 'You did not upload a valid image file. Please select a .jpg, .jpeg or .png file.')
		try:
			user_prof.save()
		except Exception as e:
			messages.error(request, 'Failed to update profile: internal server error.')
			raise
		messages.success(request, 'Your profile was updated')
		return HttpResponseRedirect(reverse('member:profile'))
	else:
		return render(request, "members/edit.html")

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
				return HttpResponseRedirect(reverse('site_info:home'))
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
	return HttpResponseRedirect(reverse('site_info:home'))

def change_password(request):
	#TODO
	pass

def reset_password(request):
	#TODO
	pass
