from django import forms
from django.core.validators import RegexValidator

from karaoke.models import Request


class RequestForm(forms.Form):
    ultrastarValidator = RegexValidator(r'^https:\/\/ultrastar-es\.org\/en\/canciones\?.*$', message="Invalid url")
    anilistValidator = RegexValidator(r'^https:\/\/anilist\.co\/anime\/[0-9]*\/?.*$', message="Invalid url")

    title = forms.CharField(label="Song title", max_length=200)
    artist = forms.CharField(label="Song artist", max_length=200)
    ultrastar_url = forms.URLField(label="Ultrastar url", validators=[ultrastarValidator])
    anilist_url = forms.URLField(label="Anilist url", validators=[anilistValidator], required=False)

    def submit(self):
        # Check request is unique
        requests = Request.objects.filter(artist=self.cleaned_data['artist'],
                                          title=self.cleaned_data['title']).distinct().order_by("title")
        if requests:
            return False
        else:
            r = Request()
            r.title = self.cleaned_data['title']
            r.artist = self.cleaned_data['artist']
            r.ultrastar_url = self.cleaned_data['ultrastar_url']
            r.anilist_url = self.cleaned_data['anilist_url']
            r.save()
            return True
