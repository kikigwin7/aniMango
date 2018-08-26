from django.shortcuts import render

from .models import Poll


def index(request):
    polls = Poll.objects.all()
    return render(request, 'polls/polls.html', {'polls': polls})


def vote(request):
    s = 1
