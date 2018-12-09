from datetime import timedelta

from django.db import models
from django.template.defaultfilters import date as d_date
from django.utils import timezone

from aniMango.bleach_html import bleach_tinymce, bleach_no_tags
from members.models import Member


class Event(models.Model):
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150)
    when = models.DateTimeField()
    where = models.CharField(max_length=100)
    details = models.TextField()
    max_signups = models.IntegerField(help_text='Set to -1 if signup is not required')
    signups_open = models.DateTimeField()
    signups_close = models.DateTimeField()

    def __str__(self):
        return '{0!s}, {1!s}, {2!s}'.format(self.title, d_date(self.when, 'D jS F Y, H:i'), self.where)

    def save(self):
        self.details = bleach_tinymce(self.details)
        super(Event, self).save()

    def week_start(self):
        # Get the day at the start of the week
        return self.when - timedelta(days=self.when.weekday())

    def signup_required(self):
        return self.max_signups > 0

    def is_full(self):
        return self.signup_required() and self.signup_set.count() >= self.max_signups

    def already_signed_up(self, member):
        return self.signup_set.filter(who=member).exists()

    def signup_count(self):
        return str(self.signup_set.count()) + '/' + str(self.max_signups)

    def opened(self):
        # Event is past the opening time. Does NOT mean that you can signup (see def closed) - Sorc
        return timezone.now() > self.signups_open

    def closed(self):
        # Event is closed past signup_close - Sorc
        return timezone.now() > self.signups_close

    class Meta:
        ordering = ['-when']


class Signup(models.Model):
    who = models.ForeignKey(Member, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField()

    def __str__(self):
        return str(self.who) + ' signup for ' + str(self.event)
