from django.db import models
from library.models import Series
from anilist_api.anilist import api_get_info
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class Showing(models.Model):
    date = models.DateField()
    SHOWING_CHOICES = (
        ('wk', 'Weekly showing'),
        ('an', 'Allnighter')
    )
    showing_type = models.CharField(
        max_length=2,
        choices=SHOWING_CHOICES,
        default='wk'
    )
    details = models.TextField(blank=True)

    def __str__(self):
        out = self.get_showing_type_display()
        return out + ' - ' + self.date.strftime('%a %d %b %Y')

class Show(models.Model):
    lib_series = models.ForeignKey(
        Series,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=110)
    title_eng = models.CharField(max_length=110)
    details = models.CharField(max_length=200)
    api_id = models.IntegerField()
    ani_link = models.URLField()
    mal_link = models.URLField(blank=True)
    wiki_link = models.URLField(blank=True)
    shown_at = models.ForeignKey(
        Showing,
        null = False,
        on_delete = models.CASCADE
    )

    def __str__(self):
        out = self.title + ' / ' + self.title_eng
        return out + ' - '+ self.shown_at.__str__()

    def nice_title(self):
        return self.title + ' / ' + self.title_eng


    # Save override to fetch the series data on creation
    def save(self, *args, **kwargs):
        # Title only exists if api data has been populated
        if self.title:
            super(Show, self).save(*args,  **kwargs) # Call real save
        else:
            # Check if the correspinig series is in the library
            try:
                lib_obj = Series.objects.get(
                    api_id=self.api_id,
                    series_type='anime'
                )
                self.lib_series = lib_obj
                self.title = lib_obj.name
                self.title_eng = lib_obj.name_eng
                self.ani_link = lib_obj.ani_link
                self.mal_link = lib_obj.mal_link
                self.wiki_link = lib_obj.wiki_link
                super(Show, self).save(*args,  **kwargs) # Call real save
                print('Used existing data')
            except ObjectDoesNotExist:
                # if not then get new api data
                api_info = api_get_info(self.api_id, 'anime')
                self.title = api_info['title_romaji']
                self.title_eng = api_info['title_english']
                # Create anilink form string + api_id
                self.ani_link = 'https://anilist.co/anime/' + str(self.api_id)
                super(Show, self).save(*args,  **kwargs) # Call real save
                print('Fetched new data')

# If a metching library series is added for an existing viewing
# Assign the foreign key for each show to the new library series
# Using django post save signals
# https://coderwall.com/p/ktdb3g/django-signals-an-extremely-simplified-explanation-for-beginners
@receiver(post_save, sender=Series)
def match_or_update_lib_series(sender, **kwargs):
    series = kwargs.get('instance')
    if kwargs.get('created', False):
        # Match existing shows by type and api_id
        # Only works for lib series using the anime api_id
        # Have to manually match manga lib series
        # TODO fix that ^^^^^^^^
        if series.series_type == 'anime':
            matched_shows = Show.objects.filter(api_id=series.api_id)
            # Sanity check for a non empty queryset
            if matched_shows:
                for show in matched_shows:
                    show.lib_series = series
                    show.ani_link = series.ani_link
                    show.mal_link = series.mal_link
                    show.save()
    # The library series has been updated, so copy across shared updated fields
    else:
        matched_shows = series.show_set.all()
        if matched_shows:
            for show in matched_shows:
                show.wiki_link = series.wiki_link
                show.mal_link = series.mal_link
                show.save()