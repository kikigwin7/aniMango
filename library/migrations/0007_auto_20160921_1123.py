# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-21 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_auto_20160806_0152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-requested', '-on_loan', 'name']},
        ),
        migrations.AddField(
            model_name='series',
            name='name_eng',
            field=models.CharField(default='english name', max_length=110),
            preserve_default=False,
        ),
    ]