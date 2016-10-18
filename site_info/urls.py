from django.conf.urls import url

from . import views

app_name = 'site_info'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^info/constitution/$', views.constitution, name='constitution'),
	url(r'^info/history/$', views.history, name='history'),
]