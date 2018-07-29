from datetime import date, timedelta
import re

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from anilist_api.anilist import populate_series_item
from showings.models import Show

# Series model to describe an anime or manga
# Will be used in library managment
class Series(models.Model):
    auto_populate_data = models.BooleanField(default=False, help_text="Check this to use AniList link to (re)populate fields. MAL and Wiki links still need to be entered manually.")#TODO: rewrite this in not hack-ish way -Sorc

    title = models.CharField(max_length=110, blank=True)
    title_eng = models.CharField(max_length=110, blank=True)
    api_id = models.IntegerField(unique=True, null=True, blank=True)
    series_type = models.CharField(max_length=10, blank=True)
    synopsis = models.TextField(blank=True)
    cover_link = models.URLField(blank=True)
    ani_link = models.URLField(blank=True)
    mal_link = models.URLField(blank=True)
    wiki_link = models.URLField(blank=True)

    cooldown_date = models.DateField(null=True, blank=True, editable=False)

    def __str__(self):
        if self.title and self.title_eng and self.series_type:
            return '{0!s}: {1!s}'.format(self.series_type, self.nice_title())
        else:
            return 'Unknown series'

    # Tell django that the plural of 'series' is 'series' for the admin screen
    class Meta:
        verbose_name_plural = "series"

    # Save override so that api data can be used for new series entries
    def save(self):
        if self.auto_populate_data:
            self.auto_populate_data = False
            values = re.split(r'\/', re.sub(r'(https:\/\/)*(www\.)*(anilist.co\/)*', '', str(self.ani_link)))
            #TODO: validate link and values - Sorc
            self.series_type = values[0]
            self.api_id = values[1]
            populate_series_item(self)
        super(Series, self).save() # Call real save

    def nice_title(self):
        return '{0!s} / {1!s}'.format(self.title, self.title_eng)

    def is_on_cooldown(self):
        if 'anime' == self.series_type and self.get_cooldown_date():
            return (self.get_cooldown_date() > date.today())
        return False

    def get_cooldown_date(self):
        return self.cooldown_date

    def cd_status(self):
        if not 'anime' == self.series_type:
            return ''
        if self.is_on_cooldown():
            return 'On cooldown until ' + self.get_cooldown_date().strftime("%Y/%m/%d")
        return 'Not on cooldown'


# Item class that repesents each library item
class Item(models.Model):
    parent_series = models.ForeignKey(Series, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False, null=False)
    MEDIA_TYPE_CHOICES = (
        ('Manga', 'Manga'),
        ('Light Novel', 'Light Novel'),
        ('Visual Novel', 'Visual Novel'),
        ('DVD', 'DVD'),
        ('BD', 'BD'),
        ('CD', 'CD'),
        ('Other', 'Other')
    )
    media_type = models.CharField(
        max_length=16,
        choices=MEDIA_TYPE_CHOICES,
        blank=False
    )
    details = models.CharField(
        max_length=64,
        blank=True
    )

    def __str__(self):
        return str(self.parent_series) + ' : ' + self.name

    def status(self):
        if not Request.objects.filter(item=self).exists():
            return 'Available'
        return Request.objects.get(item=self).status()

    def request(self, user):
        #if request for this item already exists, then it's taken and cannot be requested
        if Request.objects.filter(item=self).exists():
            return None
        r = Request()
        r.item = self
        r.status_variable = 'Requested'
        r.user = user
        r.save()
        return r

class Request(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    date_requested = models.DateTimeField(auto_now_add=True)
    return_deadline = models.DateField(blank=True, null=True, help_text='Filled automatically on approval. Default loan period - 2 weeks. Set manually to override.')
    STATUS_CHOICES = (
        ('Requested', 'Requested'),
        ('On Loan', 'On Loan'),
        ('Late', 'Late'),
    )
    #Use status_variable only for setting it. For getting use def self.status() - Sorc
    status_variable = models.CharField(max_length=16, choices=STATUS_CHOICES, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)

    def __str__(self):
        return '{0!s}: {1!s} ({2!s})'.format(self.status(), self.item.parent_series.nice_title(), self.item.name)

    def status(self):
        if self.return_deadline:
            if date.today() > self.return_deadline:
                self.status_variable = 'Late'
                self.save()
        return self.status_variable

    def approve(self):
        if self.status() == 'Requested':
            self.status_variable = 'On Loan'
            if not self.return_deadline:
                self.return_deadline = date.today() + timedelta(weeks=2)
            self.save()
            return True
        return False

    def deny(self):
        if self.status() == 'Requested':
            self.archive('Denied')
            self.delete()
            return True
        return False

    def absent(self):
        if self.status() == 'Requested':
            self.archive('Absent')
            self.delete()
            return True
        return False

    def returned(self, status):
        if 'Late' == status and not self.status() == 'Late':
            #Prevent user error when marking returned item as late when it is not late -Sorc
            return False
        if self.status() == 'On Loan' or self.status() == 'Late':
            self.archive(status)
            self.delete()
            return True
        return False

    def archive(self, status):
        r = ArchivedRequest()
        r.item = self.item
        r.date_requested = self.date_requested
        r.return_deadline = None if status == 'Denied' or status == 'Absent' else self.return_deadline
        r.date_finalised = date.today()
        r.status = status
        r.user = self.user
        r.save()

    def renew(self):
        if (self.status_variable == 'On Loan' or self.status_variable == 'Late') and self.return_deadline:
            self.return_deadline += timedelta(weeks=1)
            self.status_variable = 'On Loan'
            self.save()
            return True
        return False

    class Meta:
        ordering = ['-date_requested']

class ArchivedRequest(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date_requested = models.DateTimeField()
    date_finalised = models.DateField()
    return_deadline = models.DateField(null=True)
    STATUS_CHOICES = (
        ('Denied', 'Denied'),
        ('Late', 'Late'),
        ('Returned', 'Returned'),
        ('Absent', 'Absent'),
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


@receiver(pre_save, sender=Show)
def update_series_cooldown_pre(sender, **kwargs):
    try:
        old_show = Show.objects.get(pk=kwargs.get('instance').pk)
    except:
        return None

    lib_series = old_show.lib_series
    if not lib_series:
        return None

    if not 'anime' == lib_series.series_type:
        return None
    cd_date = date.min
    for show in Show.objects.select_related('shown_at').filter(lib_series=lib_series):
        if(show == old_show):
            continue
        d = show.shown_at.date + timedelta(days=show.cooldown_period)
        if d>cd_date:
            cd_date = d
    lib_series.cooldown_date = cd_date
    lib_series.save()

@receiver(post_save, sender=Show)
def update_series_cooldown(sender, **kwargs):
    lib_series = kwargs.get('instance').lib_series

    if not 'anime' == lib_series.series_type:
        return None
    cd_date = date.min
    for show in Show.objects.select_related('shown_at').filter(lib_series=lib_series):
        d = show.shown_at.date + timedelta(days=show.cooldown_period)
        if d>cd_date:
            cd_date = d
    lib_series.cooldown_date = cd_date
    lib_series.save()
