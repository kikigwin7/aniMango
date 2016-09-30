from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage

from .models import Series, Item

def index(request):
    template = 'library/index.html'
    # Get page number from get variable in url
    page = request.GET.get('page')
    series_list = Series.objects.order_by('title_eng')
    # 24 series per page
    paginator = Paginator(series_list, 24)

    try:
        series = paginator.page(page)
    except InvalidPage:
        # Return first page for invalid input
        series = paginator.page(1)

    context = {
        'series_l': series
    }
    return render(request, template, context)

def index_search(request):
    template ='library/search.html'
    query = request.GET.get('query')
    if query is None or query == '':
        # An empty query is redirected to the regular index
        return HttpResponseRedirect(reverse('library:index'))
    else:
        # Case insensitive filter of series title in english and romaji
        results = Series.objects.filter(
            Q(title__icontains=query)|Q(title_eng__icontains=query)
        )
        context = {
            'pre_search': query,
            'series_l': results
        }
        return render(request, template, context)

def series_view(request, series_id):
    template = 'library/view.html'
    library_series = get_object_or_404(
        Series,
        id=series_id
    )
    library_items = Item.objects.filter(parent_series=library_series)
    context = {
        'series': library_series,
        'items': library_items
    }
    return render(request, template, context)

def request_form(request, item_id):
    template = 'library/request.html'
    item = get_object_or_404(Item, id=item_id)
    parent = item.parent_series
    if request.user.is_authenticated():
        # Render form
        context = {
            'series': parent,
            'item': item
        }
        return render(request, template, context)
    else:
        # Redirect to series view with message to login
        messages.error(request, 'You must be logged in to request an item')
        # Construct redirect url using reverse()
        redir_url = reverse(
            'library:detail',
            args=[parent.id]
        )
        return HttpResponseRedirect(redir_url)

def item_get(request):
    # check for post request
    if request.method != 'POST':
        raise PermissionDenied
    # check for logged in user
    if not request.user.is_authenticated():
        raise PermissionDenied

    item_id = request.POST.get('id')
    lib_item = get_object_or_404(Item, id=item_id)

    # Sanity check
    if lib_item.status() != 'Available':
        messages.error(request, 'Error: Item unavailable')
    else:
        # Do the thing
        lib_item.requested = True
        lib_item.loan_user = request.user
        lib_item.save()
        messages.success(request, 'Item successfully requested')

    parent = lib_item.parent_series
    # Construct redirect url using reverse()
    redir_url = reverse(
        'library:detail',
        args=[parent.id]
    )
    return HttpResponseRedirect(redir_url)