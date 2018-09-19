from rest_framework import generics
from library.models import Series, Item
from .serializers import LibrarySerializer
from rest_framework import filters

class ItemRView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = LibrarySerializer
    queryset = Series.objects.all()

class LibraryRView(generics.ListAPIView):
    serializer_class = LibrarySerializer
    queryset = Series.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'title_eng', 'ani_link', 'mal_link')