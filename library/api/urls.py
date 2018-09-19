from .views import ItemRView,LibraryRView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', LibraryRView.as_view(), name='item-rud'),
    url(r'^(?P<id>[0-9]+)/$', ItemRView.as_view(), name='library-rud')
]