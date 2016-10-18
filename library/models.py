from django.db import models
# Use django settings to reference the AUTH_USER_MODEL
from django.conf import settings
# api functions
from anilist_api.anilist import api_get_info
from datetime import date

# Copy info from api to series model
def copy_info(series, info):
    series.title = info['title_romaji']
    series.title_eng = info['title_english']
    series.cover_link = info['image_url_lge']
    series.synopsis = info['description']
    if info['series_type'] == 'manga':
        # it's a mango
        if info['relations_manga']:
            series.api_anime = info['relations_manga'][0]['id']
    else:
        # it's an annie may!
        if info['relations_manga']:
            series.api_manga = info['relations_manga'][0]['id']

    if series.api_anime:
        series.ani_link = 'https://anilist.co/anime/' + str(series.api_anime)
    else:
        series.ani_link = 'https://anilist.co/manga/' + str(series.api_manga)

# Series model to describe an anime or manga
# Will be used in library managment
class Series(models.Model):
    title = models.CharField(max_length=110, blank=True)
    title_eng = models.CharField(max_length=110, blank=True)
    api_manga = models.IntegerField(unique=True, null=True)
    api_anime = models.IntegerField(unique=True, null=True)
    cover_link = models.URLField(blank=True)
    synopsis = models.TextField(blank=True)
    ani_link = models.URLField(blank=True)
    mal_link = models.URLField(blank=True)
    wiki_link = models.URLField(blank=True)

    def __str__(self):
        if self.title:
            return self.title + ' / ' + self.title_eng
        else:
            man = self.api_manga
            ani = self.api_anime
            return 'Unknown series --> Manga ID: %s, Anime ID: %s' % (man, ani)

    # Tell django that the plural of 'series' is 'series' for the admin screen
    class Meta:
        verbose_name_plural = "series"

    # Save override so that api data can be used for new series entries
    def save(self):
        # self.title should exist if api data has been populated
        if self.title:
            super(Series, self).save() # Call real save
        else:
            # get the info from the api on save if series info doesnt exist
            if self.api_anime:
                info = api_get_info(self.api_anime)
            else:
                info = api_get_info(self.api_manga)

            if info:
                copy_info(self, info)

            super(Series, self).save() # Call real save


# Item class that repesents each library item with associated loan
class Item(models.Model):
    parent_series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    MEDIA_TYPE_CHOICES = (
        ('Manga', 'Manga'),
        ('Light Novel', 'Light Novel'),
        ('DVD', 'DVD'),
        ('BD', 'BD'),
        ('Other', 'Other')
    )
    media_type = models.CharField(
        max_length=15,
        choices=MEDIA_TYPE_CHOICES,
        blank=True
    )
    details = models.CharField(
        max_length=30,
        blank=True
    )
    on_loan = models.BooleanField(default=False)
    requested = models.BooleanField(default=False)
    loan_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # Can be null if no one has taken it out
        models.SET_NULL,
        null=True
    )
    return_date = models.DateField(null=True)

    def __str__(self):
        return str(self.parent_series) + ' : ' + self.name

    def status(self):
        if self.on_loan and not self.requested:
            if not self.return_date:
                return 'On Loan'
            elif self.return_date < date.today():
                return 'Late'
            else:
                return 'On Loan'

        elif self.requested and not self.on_loan:
            return 'Requested'
        else:
            return 'Available'

    # orders by requested items first, on_loan second
    class Meta:
        ordering = ['-requested', '-on_loan','name']