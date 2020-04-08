from django.core.management.base import BaseCommand
from library.models import Series
from anilist_api.anilist import api_get_info
import time


def updateImage(item):
    data = api_get_info(item)
    try:
        item.cover_link = data['coverImage']['large']
        item.save()
    except TypeError:
        print("Failed to update")


class Command(BaseCommand):
    help = 'Displays current time'

    def add_arguments(self, parser):
        parser.add_argument('field', nargs='+', type=str)

    def handle(self, *args, **kwargs):

        print("Checking all of the series against the current values")

        library = Series.objects.all()
        count = 0
        for item in library:
            if item.api_id is not None:
                time.sleep(1)
                if kwargs["field"][0] == "image":
                    updateImage(item)
                    count += 1
                    print(count, "/", library.__len__(), " - Updating ", item.title)
                else:
                    break;
