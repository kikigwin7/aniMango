# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-10 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20161004_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='profile_url',
        ),
        migrations.AddField(
            model_name='member',
            name='img',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
