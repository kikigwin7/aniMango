# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-05 19:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0010_series_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='slug',
        ),
    ]
