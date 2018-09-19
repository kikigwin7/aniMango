from rest_framework import serializers
from library.models import Series, Item

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = [
            'id',
            'title',
            'title_eng',
            'api_id',
            'series_type',
            'synopsis',
            'cover_link',
            'ani_link',
            'mal_link',
            'wiki_link',
            'cooldown_date',
        ]