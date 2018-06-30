from django.conf.urls import url

from . import views

app_name = 'site_info'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^info/constitution/$', views.constitution, name='constitution'),
	url(r'^info/contact/$', views.contact, name='contact'),
	url(r'^info/about/$', views.about, name='about'),
	url(r'^info/gdpr/$', views.gdpr, name='gdpr'),
	url(r'^info/history/$', views.history, name='history'),
	url(r'^info/exec/(?P<year>[0-9]{4})/$', views.exec_people, name='exec'),
]
