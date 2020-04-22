from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.shortcuts import render

from karaoke.forms import RequestForm
from karaoke.models import Song, Request


def index(request):
    context = {}
    query = request.GET.get("query")

    if query:
        context["query"] = query
        songs_list = Song.objects.filter(
            (Q(title__icontains=query) | Q(artist__icontains=query)) | Q(series__title__icontains=query)
            | Q(series__title_eng__icontains=query)
        ).distinct().order_by("title")
    else:
        songs_list = Song.objects.filter().distinct().order_by("title")

    # 24 Songs per page

    paginator = Paginator(songs_list, 24)

    try:
        songs = paginator.page(request.GET.get("page"))
    except InvalidPage:
        songs = paginator.page(1)

    context["songs_list"] = songs

    return render(request, "karaoke/index.html", context)


def request_song(request):
    context = {}

    requests_list = Request.objects.filter().distinct().order_by("title")

    context["requests_list"] = requests_list

    if request.method == "POST":
        form = RequestForm(request.POST)

        if form.is_valid():
            added = form.submit()
            if added:
                return render(request, "karaoke/request_success.html", context)
            else:
                return render(request, "karaoke/request_duplicate.html", context)
        else:
            context["form"] = form
            return render(request, "karaoke/request_form.html", context)

    return render(request, "karaoke/request_form.html", context)


def mapping_guide(request):
    return render(request, "karaoke/mapping_guide.html")
