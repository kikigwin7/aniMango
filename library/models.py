from django.db import models
# Use django settings to reference the AUTH_USER_MODEL
from django.conf import settings
# api functions
from .anilist import api_get_info
from datetime import date

# Series model to describe an anime or manga
# Will be used in library managment
class Series(models.Model):
    name = models.CharField(max_length=110)
    api_id = models.IntegerField()
    SERIES_TYPE_CHOICES = (
        ('manga', 'API id is for Manga'),
        ('anime', 'API id is for Anime')
    )
    series_type = models.CharField(
        max_length=5,
        choices=SERIES_TYPE_CHOICES,
        default='manga'
    )
    cover_link = models.URLField()
    synopsis = models.TextField()
    ani_link = models.URLField()
    mal_link = models.URLField(blank=True)
    wiki_link = models.URLField(blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return 'Unknown %s --> API ID: %s' % (self.media_type, self.api_id)

    # Tell django that the plural of 'series' is 'series' for the admin screen
    class Meta:
        verbose_name_plural = "series"

    def save(self, *args, **kwargs):
        #Check if series info is set by the api
        if self.name:
            super(Series, self).save(*args,  **kwargs) # Call real save
        else:
            # get the info from the api on save if series info doesnt exist
            api_info = api_get_info(self.api_id, self.series_type)
            self.name = api_info['title_romaji']
            self.cover_link = api_info['image_url_lge']
            self.synopsis = api_info['description']
            link = 'https://anilist.co/'
            link += self.series_type + '/'
            link += str(self.api_id)
            self.ani_link = link
            super(Series, self).save(*args,  **kwargs) # Call real save

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
        return self.parent_series.name + ' : ' + self.name

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