from django.conf.urls import url

from . import views

app_name = 'events'

urlpatterns = [
	url(r'^$', views.upcoming, name='upcoming'),
	url(r'^previous/$', views.previous, name='previous'),
	url(r'^(?P<event_id>[0-9]+)/$', views.event_view, name='view'),
	url(r'^(?P<event_id>[0-9]+)/signup/$', views.signup, name='signup'),
]