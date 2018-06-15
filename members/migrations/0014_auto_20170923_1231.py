# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-23 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_auto_20170911_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='nick',
            field=models.CharField(blank=True, default=members.models.get_rand_nick, max_length=30),
        ),
    ]