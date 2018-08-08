from django.conf.urls import url, include

from . import views

app_name = 'member'

urlpatterns = [
    # TODO, auth views for account stuff
    # url(r'^', include('django.contrib.auth.urls')),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.view, name='view_member'),
    url(r'^edit/$', views.profile_edit, name='edit'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
