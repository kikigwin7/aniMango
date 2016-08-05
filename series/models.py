from django.db import models
# Use django settings to reference the AUTH_USER_MODEL
from django.conf import settings
# api functions
from .anilist import api_get_info

# Series model to describe an anime or manga
# Will be used in both viewings and library managment
class Series(models.Model):
    name = models.CharField(max_length=110)
    api_id = models.IntegerField()
    MEDIA_TYPE_CHOICES = (
        ('manga', 'API id is for Manga'),
        ('anime', 'API id is for Anime')
    )
    media_type = models.CharField(
        max_length=5,
        choices=MEDIA_TYPE_CHOICES,
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
            api_info = api_get_info(self.api_id, self.media_type)
            self.name = api_info['title_romaji']
            self.cover_link = api_info['image_url_lge']
            self.synopsis = api_info['description']
            self.ani_link = 'https://anilist.co/'+self.media_type+'/'+self.api_id
            super(Series, self).save(*args,  **kwargs) # Call real save