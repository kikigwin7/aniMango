from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^(?P<media_type>manga)/(?P<series_id>.+)/$', views.series_view),
	url(r'^(?P<media_type>anime)/(?P<series_id>.+)/$', views.series_view)
]