from django.conf.urls import url

from . import views

app_name = 'forum'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^board/(?P<board_id>[0-9]+)/$', views.board, name='board'),
    url(r'^board/(?P<board_id>[0-9]+)/new/$', views.new, name='new'),
    url(r'^thread/(?P<thread_id>[0-9]+)/$', views.thread, name='thread'),
    url(r'^thread/(?P<thread_id>[0-9]+)/reply/$', views.reply, name='reply'),
    url(r'^thread/(?P<post_id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^thread/(?P<post_id>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^thread/(?P<thread_id>[0-9]+)/pin/$', views.pin, name='pin'),
]
