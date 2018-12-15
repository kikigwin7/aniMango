from django.conf.urls import url

from . import views

app_name = 'archive'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^item/(?P<id>[0-9]+)$', views.item, name='item'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)$', views.month, name='month'),
    url(r'^(?P<year>[0-9]+)$', views.year, name='year'),
]
