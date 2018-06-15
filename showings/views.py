from datetime import date

from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.shortcuts import render

from .models import Showing, Show

#All your search and not search needs in one place (as long as template is not missing any var assignments in links and etc.) - Sorc
def schedule(request):
	context = {}
	year = request.GET.get('year')
	if year:
		context['year'] = year
	query = request.GET.get('query')
	if query:
		context['query'] = query
	
	paginator = Paginator(get_showings(year, query), 10)
	try:
		showing_page = paginator.page(request.GET.get('page'))
	except InvalidPage:
		showing_page = paginator.page(1)
	
	if request.GET.get('cd_search'):
		context['cd_search'] = True
	context['showing_page'] = showing_page
	context['date_range'] = get_date_range()
	return render(request, 'showings/schedule.html', context)
		
def get_showings(year, query):
	showings = Showing.objects
	if year and isint(year):
		start_date = date(int(year), 8, 1)
		end_date = date(int(year)+1, 8, 1)
		showings = showings.filter(date__gte=start_date, date__lt=end_date)
	if query:
		showings = showings.filter(
			Q(show__lib_series__title__icontains=query)|Q(show__lib_series__title_eng__icontains=query)
		).distinct()
	return showings.order_by('-date')
	
def get_date_range():
	return reversed(list(range(2003, date.today().year+1)))
	
def isint(value):
	try:
		int(value)
		return True
	except:
		return False