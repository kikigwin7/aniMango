from django.conf.urls import url

from . import views

app_name = 'polls'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^poll/(?P<post_id>[0-9]+)/vote$', views.vote, name='vote'),
]
