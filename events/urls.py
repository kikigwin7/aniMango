from django.conf.urls import url

from . import views

app_name = 'events'

urlpatterns = [
    url(r'^(?P<page>[0-9]+)/$', views.upcoming, name='upcoming'),
    url(r'^previous/(?P<page>[0-9]+)/$', views.previous, name='previous'),
    url(r'^event_detail/(?P<event_id>[0-9]+)/$', views.event_view, name='view'),
    url(r'^event_detail/(?P<event_id>[0-9]+)/signup/$', views.signup, name='signup'),
    url(r'^event_detail/(?P<event_id>[0-9]+)/cancel/$', views.cancel, name='cancel')
]
