from django.conf.urls import url

from . import views

app_name = 'news'

urlpatterns = [
	url(r'^article/(?P<article_id>[0-9]+)/(?P<article_slug>.+)/$', views.article, name='article'),
	url(r'^(?P<category>.+)/(?P<page>[0-9]+)/$', views.latest, name='latest'),
]