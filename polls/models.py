from django.db import models
from django.http import HttpResponse


class Poll(models.Model):
    name = models.CharField(max_length=30, help_text='Enter name of poll')
    description = models.CharField(max_length=50, help_text='Description of the poll', null=True)
    open = models.BooleanField(default=True)

    def results(request):
        return HttpResponse('')

    def vote(request):
        print("Results")

    def __str__(self):
        return self.name


class Option(models.Model):
    lib_series = models.ForeignKey(
        'library.Series',
        null=True,
        on_delete=models.PROTECT
    )

    memberOf = models.ForeignKey(
        Poll,
        null=False,
        on_delete=models.CASCADE
    )

    details = models.CharField(
        max_length=200,
        null=True,
        help_text='Episodes watched (Ep.1, Eps. 1-3), etc.'

    )

    votes = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return '{0!s}'.format(self.lib_series.nice_title())

    def save(self):
        super(Option, self).save()


class Voter(models.Model):
    memberOf = models.ForeignKey(
        Poll,
        null=False,
        editable=False
    )

    voter_id = models.CharField(max_length=30, default='', editable=False)
