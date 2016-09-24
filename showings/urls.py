from django.conf.urls import url

from . import views

app_name = 'showings'

urlpatterns = [
	url(r'^schedule/$', views.schedule, name='schedule'),
	url(r'^year/(?P<year>[0-9]{4})/$', views.year, name='year'),
	url(r'^cooldown/$', views.cooldown, name='cooldown')
]