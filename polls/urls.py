from django.conf.urls import url

from . import views

app_name = 'polls'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9]+)/vote$', views.vote, name='vote'),
    url(r'^view/(?P<post_id>[0-9]+)', views.view, name='view'),
    url(r'^results/(?P<post_id>[0-9]+)$', views.results, name='results'),
]
