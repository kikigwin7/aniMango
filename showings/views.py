from django.shortcuts import render
from django.db.models import Q
from .models import Showing, Show
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage

# Create your views here.

def schedule(request):
	template = 'showings/schedule.html'
	page_no = request.GET.get('page')
	showings_list = Showing.objects.order_by('date')
	paginator = Paginator(showings_list, 20) # 20 Showings per page
	try:
		showing_page = paginator.page(page_no)
	except InvalidPage:
		# Return first page for invalid page
		showing_page = paginator.page(1)

	context = {
		'showing_page': showing_page
	}
	return render(request, template, context)

def year(request, year):
	template = 'showings/by_year.html'
	context = {
		'year': year
	}
	return render(request, template, context)

def cooldown(request):
	template = 'showings/cooldown.html'
	query = request.GET.get('query')
	if query is None or query == '':
		return HttpResponseRedirect(reverse('showings:schedule'))
	else:
		results = Show.objects.filter(
			Q(title__icontains=query)|Q(title_eng__icontains=query)
		)
		context = {
			'pre_search': query,
			'shows_l': results
		}
		return render(request, template, context)