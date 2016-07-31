from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	response = "This is the members index"
	return HttpResponse(response)