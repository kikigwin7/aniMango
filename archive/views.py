from .models import Item
from django.shortcuts import render
import calendar
import math, re

def index(request):
    # Display all of the different Directories with the years
    items = Item.objects.all()
    years = set()
    for object in items:
        if object.date.year not in years:
            years.add(object.date.year)

    year_data = list()
    for year in years:
        year_data.append({'year': year, 'numItems': items.filter(date__year=year).count()})
    context = {
        'years': year_data
    }
    return render(request, 'archive/index.html', context)


def year(request, year):
    # Display all of the different Directories with the years
    items = Item.objects.filter(date__year=year)
    months = set()
    for object in items:
        if object.date.month not in months:
            months.add(object.date.month)

    month_data = list()
    for month_item in months:
        month_data.append({'month': month_item, 'monthName': calendar.month_name[month_item],
                          'numItems': items.filter(date__month=month_item).count()})
    context = {
        'yearDate': year,
        'months': month_data,
    }
    return render(request, 'archive/year.html', context)


def month(request, year, month):
    items = Item.objects.filter(date__year=year, date__month=month)
    context = {
        'items': items,
    }
    return render(request, 'archive/month.html', context)


def item(request, id):
    item = Item.objects.get(id=id)
    file_size = math.ceil(item.file.size / 1024)
    raw_name = re.sub(r"^(.*?)/", "", str(item.file.name))
    context = {
        'item': item,
        'size': file_size,
        'raw_name': raw_name,
    }
    return render(request, 'archive/item.html', context)
