from datetime import date

from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.shortcuts import render

from .models import Showing, Show


# All your search and not search needs in one place (as long as template is not missing any var assignments in links
# and etc.) - Sorc
def schedule(request):
    context = {}
    year = request.GET.get('year')
    show_type = request.GET.get('type')
    if year:
        context['year'] = year
    if show_type:
        context['type'] = show_type
    query = request.GET.get('query')
    if query:
        context['query'] = query

    paginator = Paginator(get_showings(year, show_type, query), 10)
    try:
        showing_page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        showing_page = paginator.page(1)

    if request.GET.get('cd_search'):
        context['cd_search'] = True
    context = {
        'showing_page': showing_page,
        'date_range': get_date_range(),
        'showing_types': Showing.SHOWING_CHOICES,
        'year': year,
        'type': show_type,
    }
    return render(request, 'showings/schedule.html', context)


# Simple way to filter out the showings into the way described by the user
# Add a new if statement for each of the filters possible
def get_showings(year, show_type, query):
    showings = Showing.objects
    if year and isint(year):
        start_date = date(int(year), 8, 1)
        end_date = date(int(year) + 1, 8, 1)
        showings = showings.filter(date__gte=start_date, date__lt=end_date)

    if show_type and show_type != 'all':
        showings = showings.filter(showing_type=show_type)

    if query:
        showings = showings.filter(
            Q(show__lib_series__title__icontains=query) | Q(show__lib_series__title_eng__icontains=query)
        ).distinct()

    return showings.order_by('-date')


# Returns a range of dates between 2003 and the current year + 1
def get_date_range():
    return reversed(list(range(2003, date.today().year + 1)))


def isint(value):
    try:
        int(value)
        return True
    except:
        return False
