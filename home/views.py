from django.shortcuts import render

def home(request):
	template = 'home/home.html'
	return render(request, template)