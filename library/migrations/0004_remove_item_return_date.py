# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-06 01:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20160806_0131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='return_date',
        ),
    ]