from django.conf.urls import url

from . import views

app_name = 'showings'

urlpatterns = [
	url(r'^schedule/$', views.schedule, name='schedule'),
]