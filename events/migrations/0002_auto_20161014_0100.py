# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-14 01:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='max_signups',
            field=models.IntegerField(help_text='Set to -1 for unlimited signups'),
        ),
    ]
