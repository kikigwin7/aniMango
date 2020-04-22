import re

from django.db import models

from library.models import Series


class Song(models.Model):
    title = models.CharField(max_length=200, blank=False)
    artist = models.CharField(max_length=200, blank=False)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '{0!s} - {1!s}'.format(self.artist, self.title)

    class Meta:
        verbose_name_plural = "songs"


class Request(models.Model):
    title = models.CharField(max_length=200, blank=False)
    artist = models.CharField(max_length=200, blank=False)
    anilist_url = models.URLField()
    ultrastar_url = models.URLField(blank=False, unique=True)

    def __str__(self):
        return '{0!s} - {1!s}'.format(self.artist, self.title)

    class Meta:
        verbose_name_plural = "requests"

    def complete(self):
        s = Song()
        s.title = self.title
        s.artist = self.artist
        # Add show
        if self.anilist_url:
            values = re.split(r'\/', re.sub(r'(https:\/\/)*(www\.)*(anilist.co\/)*', '', str(self.anilist_url)))
            api_id = values[1]
            try:
                show = Series.objects.get(api_id=api_id)
            except Series.DoesNotExist:
                # Make series
                new_series = Series()
                new_series.auto_populate_data = True
                new_series.ani_link = self.anilist_url
                new_series.save()
                show = new_series
            s.series = show

        s.save()
        self.archive("Completed", s)

    def remove(self):
        self.archive("Cancelled")

    def archive(self, status, song=None):
        r = ArchivedRequest()
        r.ultrastar_url = self.ultrastar_url
        r.status = status
        if song is not None:
            r.related_song = song
        r.save()
        self.delete()


class ArchivedRequest(models.Model):
    related_song = models.ForeignKey(Song, null=True, blank=True, on_delete=models.CASCADE)
    ultrastar_url = models.URLField(blank=False)

    STATUS_CHOICES = (
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled")
    )

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, blank=False)

    def __str__(self):
        return "{0!s} - {1!s}".format(self.ultrastar_url, self.status)
