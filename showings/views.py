from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage
from datetime import date, timedelta

from .models import Showing, Show

def schedule(request):
	template = 'showings/schedule.html'
	showings_list = Showing.objects.order_by('-date')
	paginator = Paginator(showings_list, 10) # 10 Showings for recent
	showing_page = paginator.page(1)

	# Get the earliest year any showing was shown
	if Showing.objects.order_by('date'):
		earliest_year = Showing.objects.order_by('date')[0].date.year
		# Get the range of dates of showings as a list
		date_range = list(range(earliest_year, date.today().year))
		date_range.append(date.today().year)
	else:
		date_range = None

	context = {
		'showing_page': showing_page,
		'date_range': date_range
	}
	return render(request, template, context)

def year(request):
	template = 'showings/by_year.html'
	page_no = request.GET.get('page')
	year = request.GET.get('year')
	if year is None or year == '':
		return HttpResponseRedirect(reverse('showings:schedule'))
	elif year == 'All':
		showings_list = Showing.objects.order_by('-date')
	else:
		try:
			year = int(year) # Should throw exception if not int
			showings_list = Showing.objects.filter(date__year=year).order_by('-date')
		except:
			return HttpResponseRedirect(reverse('showings:schedule'))

	paginator = Paginator(showings_list, 10) # 10 Showings per page
	try:
		showing_page = paginator.page(page_no)
	except InvalidPage:
		# Return first page for invalid page
		showing_page = paginator.page(1)

	# Get the earliest year any showing was shown
	if Showing.objects.order_by('date'):
		earliest_year = Showing.objects.order_by('date')[0].date.year
		# Get the range of dates of showings as a list
		date_range = list(range(earliest_year, date.today().year))
	else:
		date_range = None
	
	context = {
		'year': year,
		'showing_page': showing_page,
		'date_range': date_range
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
		).order_by('-shown_at__date')

		prev_show = None
		non_duplicate_show_list = []
		for show in results:
			if prev_show is None:
				prev_show = show
				non_duplicate_show_list.append(show)
			else:
				if prev_show.anilist_anime_number == show.anilist_anime_number:
					pass
				else:
					prev_show = show
					non_duplicate_show_list.append(show)

		# Python doesnt have timedelta in years, y tho
		year = timedelta(days=365)
		# Cooldown includes upto two years ago
		two_years_ago = date.today() - year - year
		context = {
			'pre_search': query,
			'shows_l': non_duplicate_show_list,
			'cd_date': two_years_ago
		}
		return render(request, template, context)

def search(request):
	template = 'showings/search.html'
	query = request.GET.get('query')
	if query is None or query == '':
		return HttpResponseRedirect(reverse('showings:schedule'))
	else:
		results = Show.objects.filter(
			Q(title__icontains=query)|Q(title_eng__icontains=query)
		).order_by('-shown_at__date')

		context = {
			'pre_search': query,
			'shows_l': results
		}
		return render(request, template, context)