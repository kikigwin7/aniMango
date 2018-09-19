from .views import EventRView, EventsRView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', EventsRView.as_view(), name='post-rud'),
    url(r'^(?P<id>[0-9]+)/$', EventRView.as_view(), name='post-rud')
]