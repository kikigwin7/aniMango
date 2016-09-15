from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse

from .models import Series, Item

def index(request):
    template = 'library/index.html'
    series_list = Series.objects.order_by('name')
    context = {
        'series_list': series_list
    }
    return render(request, template, context)

def series_view(request, media_type, series_id):
    template = 'library/view.html'
    library_series = get_object_or_404(
        Series,
        api_id=series_id,
        series_type=media_type
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
            args=[parent.series_type, parent.api_id]
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
        raise PermissionDenied

    lib_item.requested = True
    lib_item.loan_user = request.user
    lib_item.save()

    parent = lib_item.parent_series

    # Redirect to series view with success message
    messages.success(request, 'Item successfully requested')
    # Construct redirect url using reverse()
    redir_url = reverse(
        'library:detail',
        args=[parent.series_type, parent.api_id]
    )
    return HttpResponseRedirect(redir_url)