from django.shortcuts import render
from django.http import HttpResponse

from series.models import Series

# Create your views here.

def index(request):
	response = "This is the library index"
	return HttpResponse(response)