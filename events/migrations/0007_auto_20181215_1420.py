# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-12-15 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20170814_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='who',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='members.Member'),
        ),
    ]
