from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index),
	# regex for any character string as one token
	url(r'^(?P<id>.+)/$', views.series_view)
]