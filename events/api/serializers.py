from rest_framework import serializers
from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'subtitle',
            'when',
            'where',
            'details',
            'max_signups',
            'signups_open',
            'signups_close',
        ]