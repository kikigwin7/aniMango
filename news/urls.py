from django.conf.urls import url

from . import views

app_name = 'news'

urlpatterns = [
	url(r'^$', views.latest, name='latest'),
	url(r'^category/$', views.category, name='category'),
	url(r'^article/(?P<article_slug>.+)/$', views.article, name='article'),
]