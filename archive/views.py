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

    yearData = list()
    for year in years:
        yearData.append({'year': year, 'numItems': items.filter(date__year=year).count()})
    return render(request, 'archive/index.html', {'years': yearData})


def year(request, year):
    # Display all of the different Directories with the years
    items = Item.objects.filter(date__year=year)
    months = set()
    for object in items:
        if object.date.month not in months:
            months.add(object.date.month)

    monthData = list()
    for month in months:
        monthData.append({'month': month, 'monthName': calendar.month_name[month],
                          'numItems': items.filter(date__month=month).count()})
    return render(request, 'archive/year.html', {'yearDate': year, 'months': monthData})


def month(request, year, month):
    items = Item.objects.filter(date__year=year, date__month=month)
    return render(request, 'archive/month.html', {'items': items})


def item(request, id):
    item = Item.objects.get(id=id)
    filesize = math.ceil(item.file.size / 1024)
    name_raw = re.sub(r"^(.*?)/", "", str(item.file.name))
    return render(request, 'archive/item.html', {'item': item, "size": filesize, "raw_name": name_raw})
