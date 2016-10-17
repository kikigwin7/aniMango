from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Event, Signup
from members.models import Member
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage
from collections import OrderedDict


# Create your views here.

def upcoming(request):
	template = 'events/list.html'
	events = Event.objects.filter(when__gte=timezone.now())

	# Solution copied from uwcs-zarya
	#
	weeks_dict = OrderedDict()
	for event in events:
		event_week = event.when.isocalendar()[1]
		key = '{year}-{week}'.format(year=event.when.year, week=event_week)

		if weeks_dict.get(key):
			weeks_dict.get(key).append(event)
		else:
			weeks_dict[key] = [event]

	weeks = list()

	for _, week in weeks_dict.items():
		weeks.append(week)
	#

	list_type = 'Upcoming'
	context = {
		'weeks': weeks,
		'list_type': list_type
	}
	return render(request, template, context)

def previous(request):
	template = 'events/list.html'
	page = request.GET.get('get')
	events = Event.objects.filter(when__lt=timezone.now())
	list_type = 'Previous'
	paginator = Paginator(events, 24)

	try:
		event_page = paginator.page(page)
	except InvalidPage:
		# Return first page for invalid input
		event_page = paginator.page(1)

	context = {
		'events_l': event_page,
		'list_type': list_type
	}
	return render(request, template, context)

def event_view(request, event_id):
	template = 'events/view.html'
	event = get_object_or_404(Event, id=event_id)
	if event.max_signups < 0:
		# No signups required
		signups = None
		signup_required = False
	else:
		signups = Signup.objects.filter(event=event)
		signup_required = True

	context = {
		'event': event,
		'signups': signups,
		'signup_required': signup_required
	}
	return render(request, template, context)

def signup(request, event_id):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('events:view', args=[event_id]))

	elif not request.user.is_authenticated():
		messages.error(request, 'You must be logged in to signup for an event')
		return HttpResponseRedirect(reverse('events:view', args=[event_id]))

	try:
		event = Event.objects.get(id=event_id)

		if event.is_full():
			messages.error(request, 'Event is full')
			return HttpResponseRedirect(reverse('events:view', args=[event_id]))

		elif event.already_signed_up(request.user.member):
			messages.error(request, 'You have already signed up for this event')
			return HttpResponseRedirect(reverse('events:view', args=[event_id]))

		new_signup = Signup(
			who=request.user.member,
			event = Event.objects.get(id=event_id),
			comment = request.POST['signup_comment'],
			created = timezone.now()
		)
		new_signup.save()
		messages.success(request, 'Signup for event successful')
		return HttpResponseRedirect(reverse('events:view', args=[event_id]))
	except ObjectDoesNotExist:
		messages.error(request, 'That event does not exist')
		return HttpResponseRedirect(reverse('events:upcoming'))
		