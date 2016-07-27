from django.db import models
# Use django settings to reference the AUTH_USER_MODEL
from django.conf import settings

# Series model to describe an anime or manga
# Will be used in both viewings and library managment
class Series(models.Model):
    name = models.CharField(max_length=110)
    api_id = models.CharField(
        max_length=20,
        blank=True
    )
    cover_link = models.URLField(blank=True)
    synopsis = models.TextField(blank=True)
    mal_link = models.URLField(blank=True)
    wiki_link = models.URLField(blank=True)

    def __str__(self):
        return self.name

    # Tell django that the plural of 'series' is 'series' for the admin interface
    class Meta:
        verbose_name_plural = "series"