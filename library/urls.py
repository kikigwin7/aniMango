from django.conf.urls import url

from . import views

app_name = 'library'
urlpatterns = [
	url(r'^$', views.index, name='index'),

	url(
		r'^series/(?P<series_id>[0-9]+)/$',
		views.series_view,
		name='detail'
	),

	url(
		r'^item/(?P<item_id>[0-9]+)/$',
		views.request_form,
		name='request_form'
	),

	url(
		r'^request/$',
		views.item_get,
		name='request_item'
	)
]