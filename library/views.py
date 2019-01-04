from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import InvalidPage, Paginator
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import Series, Item


# Combined library index and library search into one - Sorc
def index(request):
    context = {}
    query = request.GET.get('query')


    if query:
        context['query'] = query
        series_list = Series.objects.filter(
            Q(item__isnull=False) &
            (Q(title__icontains=query) | Q(title_eng__icontains=query))
        ).distinct().order_by('title')
    else:
        series_list = Series.objects.filter(item__isnull=False).distinct().order_by('title')

    # 24 series per page

    paginator = Paginator(series_list, 24)

    try:
        series = paginator.page(request.GET.get('page'))
    except InvalidPage:
        series = paginator.page(1)

    context['series_l'] = series
    return render(request, 'library/index.html', context)


def series_view(request, series_id):
    library_series = get_object_or_404(Series, id=series_id)
    context = {
        'series': library_series,
        'items': Item.objects.filter(parent_series=library_series)
    }
    return render(request, 'library/view.html', context)


@login_required
def request_form(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    context = {
        'series': item.parent_series,
        'item': item
    }
    return render(request, 'library/request.html', context)


@login_required
def item_get(request):
    # check for post request
    if request.method != 'POST':
        raise PermissionDenied

    lib_item = get_object_or_404(Item, id=request.POST.get('id'))

    # Sanity check
    if not lib_item.request(request.user):
        messages.error(request, 'Error: Item unavailable')
    else:
        messages.success(request, 'Item successfully requested')

    parent = lib_item.parent_series
    # Construct redirect url using reverse()
    return HttpResponseRedirect(reverse('library:detail', args=[parent.id]))
