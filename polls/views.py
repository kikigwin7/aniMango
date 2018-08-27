from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Poll, Option, Voter


def index(request):
    polls = Poll.objects.all()
    return render(request, 'polls/polls.html', {'polls': polls})


def results(request, post_id):
    poll = Poll.objects.get(id=post_id)
    options = poll.option_set.all()
    return render(request, 'polls/results.html', {'poll': poll, 'options': options})


def view(request, post_id):
    poll = Poll.objects.get(id=post_id)
    return render(request, 'polls/view.html', {'poll': poll})


@login_required
def vote(request, post_id):
    # TODO: You were working from here
    poll = get_object_or_404(Poll, id=post_id)
    if request.method == 'POST':
        if len(request.POST.getlist('options')) > 0:
            try:
                voter = Voter.objects.get(memberOf=poll, voter_id=request.user.id)
                messages.error(request, 'You have already voted!')
            except Voter.DoesNotExist:
                addVote(poll, request)
                voter = Voter(voter_id=request.user.id, memberOf=poll)
                voter.save()
                messages.info(request, 'Vote cast!')
        else:
            messages.error(request, 'You must select an option!')
    return HttpResponseRedirect(reverse('polls:index'))


def addVote(poll, request):
    options = request.POST.getlist('options')
    for option_id in options:
        try:
            option = Option.objects.get(memberOf=poll, lib_series_id=option_id)
            option.votes += 1
            option.save()
        except Exception as e:
            print(e.message)
