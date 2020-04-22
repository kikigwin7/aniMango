from django.conf.urls import url

from . import views

app_name = 'karaoke'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^requests/$', views.request_song, name="request_song"),
    url(r'^guide/$', views.mapping_guide, name="mapping_guide")
]