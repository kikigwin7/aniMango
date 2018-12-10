from django.core.management.base import BaseCommand
from library.models import Series
from anilist_api.anilist import api_get_info
import time

def updateImage(item):
    data = api_get_info(item)
    print('Updated the picture of ' + item.title + ' to ' + data['coverImage']['large'])
    item.cover_link = data['coverImage']['large']
    item.save()

class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('field', nargs='+', type=str)

    def handle(self, *args, **kwargs):

        print("Checking all of the series against the current values")

        library = Series.objects.all()
        for item in library:
            time.sleep(1)
            if kwargs["field"][0] == "image":
                updateImage(item)
            else:
                break;

