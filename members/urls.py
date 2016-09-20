from django.conf.urls import url

from . import views

app_name = 'member'

urlpatterns = [
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^edit/$', views.profile_edit, name='edit'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
]