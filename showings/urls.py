from django.conf.urls import url

from . import views

app_name = 'showings'

urlpatterns = [
	url(r'^schedule/$', views.schedule, name='schedule'),
	url(r'^year/$', views.year, name='year'),
	url(r'^search/$', views.search, name='search'),
	url(r'^cooldown/$', views.cooldown, name='cooldown')
]