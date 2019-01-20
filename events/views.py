from collections import OrderedDict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Event, Signup


# Create your views here.
def upcoming(request, page):
    return render(request, 'events/list.html', get_context(page, 'Upcoming'))


def previous(request, page):
    return render(request, 'events/list.html', get_context(page, 'Previous'))


# puting duplicate code from upcoming/previous in one place - Sorc
def get_context(page, event_type):
    if 'Upcoming' == event_type:
        events_all = Event.objects.filter(when__gte=timezone.now()).order_by('when')
    else:
        events_all = Event.objects.filter(when__lte=timezone.now()).order_by('-when')

    paginator = Paginator(events_all, 12)
    try:
        events_page = paginator.page(page)
    except InvalidPage:
        events_page = paginator.page(1)
    events = events_page if 'Upcoming' == event_type else events_page

    # Solution copied from uwcs-zarya
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

    return {
        'weeks': weeks,
        'paginator_page': events_page,
        'list_type': event_type,
    }


def event_view(request, event_id):
    template = 'events/view.html'
    event = get_object_or_404(Event, id=event_id)

    if not event.signup_required():
        context = {
            'event': event,
            'signup_required': False,
        }
        return render(request, template, context)

    user_is_signed_up = False if not request.user.is_authenticated else event.already_signed_up(request.user.member)
    context = {
        'event': event,
        'signups': Signup.objects.filter(event=event).order_by("-created"),
        'signup_required': True,
        'user_is_signed_up': user_is_signed_up,
        'event_is_full': event.is_full(),
        'closed': event.closed(),
        'opened': event.opened()
    }
    return render(request, template, context)


@login_required
def signup(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        if event.is_full():
            messages.error(request, 'Event is full')
        elif not event.signup_required():
            messages.error(request, 'Signups are not required for this event')
        elif event.already_signed_up(request.user.member):
            messages.error(request, 'You have already signed up for this event')
        elif event.closed():
            messages.error(request, 'Signups for this event are closed')
        elif not event.opened():
            messages.error(request, 'Signups for this event are not open yet')
        else:
            new_signup = Signup(
                who=request.user.member,
                event=Event.objects.get(id=event_id),
                comment=request.POST['signup_comment'],
                created=timezone.now()
            )
            new_signup.save()
            messages.success(request, 'Signup for event successful')
    return HttpResponseRedirect(reverse('events:view', args=[event.id]))


@login_required
def cancel(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        if event.closed():
            messages.error(request, 'Signups for this event are closed')
        else:
            Signup.objects.filter(event=event, who=request.user.member).delete();
            messages.success(request, 'Canceling successful')
    return HttpResponseRedirect(reverse('events:view', args=[event.id]))
