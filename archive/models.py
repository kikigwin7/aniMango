from django.db import models
import os


def upload_path(filename, date):
    name, ext = os.path.splitext(filename.name)
    return 'archive/{0!s}{1!s}{2!s}'.format(name, date, ext)


class Item(models.Model):
    name = models.CharField(
        null=True,
        blank=True,
        max_length=40,
        help_text='Displayed name rather than '
                  'file name (Note. filename will still be shown)'
    )

    TYPE_CHOICES = (
        ('im', 'Image'),
        ('tx', 'Text File'),
        ('we', 'Website File')
    )

    type = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default='tx'
    )

    date = models.DateField(
        null=False,
        help_text='Date of creation or last known time'
    )

    file = models.FileField(
        null=False,
        blank=False,
        upload_to='archive/',
        help_text='The file that should be uploaded'
    )

    details = models.TextField(
        null=True,
        blank=True,
        help_text='Any details about the item'
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.type == 'im':
            s = 1