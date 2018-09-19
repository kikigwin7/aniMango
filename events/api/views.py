from rest_framework import generics
from events.models import Event
from .serializers import EventSerializer
from rest_framework import filters
class EventRView(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = EventSerializer
    queryset = Event.objects.all()

class EventsRView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (filters.OrderingFilter,)
    ordering_field = ('when')
