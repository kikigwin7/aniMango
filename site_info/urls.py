from django.conf.urls import url

from . import views

app_name = 'site_info'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^info/constitution/$', views.constitution, name='constitution'),
	url(r'^info/history/$', views.history, name='history'),
	url(r'^info/exec/$', views.exec_people, name='exec'),
]