# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 16:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showings', '0002_auto_20160930_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='showing',
            name='additional_details',
        ),
    ]
