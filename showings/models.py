from django.db import models


# Create your models here.
class Showing(models.Model):
    date = models.DateField()
    SHOWING_CHOICES = (
        ('wk', 'Weekly showing'),
        ('an', 'Allnighter'),
        ('ev', 'Event'),
        ('mo', 'Movie Night'),
        ('ot', 'Other'),
    )
    showing_type = models.CharField(
        max_length=2,
        choices=SHOWING_CHOICES,
        default='wk'
    )
    details = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Brief event explanation, etc.'
    )

    def __str__(self):
        return '{0!s} - {1!s}'.format(self.get_showing_type_display(), self.date.strftime('%a %d %b %Y'))

    class Meta:
        ordering = ['-date']


class Show(models.Model):
    lib_series = models.ForeignKey(
        'library.Series',
        null=False,
        on_delete=models.PROTECT
    )
    details = models.CharField(
        max_length=200,
        help_text='Episodes watched (Ep.1, Eps. 1-3), etc.'
    )
    shown_at = models.ForeignKey(
        Showing,
        null=False,
        on_delete=models.CASCADE
    )
    TYPE_CHOICES = (
        ('ms', 'Main series'),
        ('mc', 'Main series candidate'),
        ('ex', 'Exec choice'),
        ('an', 'Allnighter'),
        ('ot', 'Other'),
    )
    show_type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        null=False,
        blank=False,
    )
    cooldown_period = models.IntegerField(default=0, null=True, blank=True,
                                          help_text="In days. Will be filled when saving according to type of show. "
                                                    "Input the value manually to override.")

    def __str__(self):
        return '{0!s} - {1!s}'.format(self.lib_series.nice_title(), self.shown_at.__str__())

    def save(self):
        if not self.cooldown_period:
            cds = {  # cooldowns for types in days
                'ms': 1095,
                'mc': 730,
                'ex': 730,
                'an': 90,
                'ot': 30,
            }
            self.cooldown_period = cds[self.show_type]
        super(Show, self).save()
