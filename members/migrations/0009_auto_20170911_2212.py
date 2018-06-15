# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-11 22:12
from __future__ import unicode_literals

from django.db import migrations, models
import members.models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20170911_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='img_height',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='img_width',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='img',
            field=models.ImageField(blank=True, height_field=b'img_height', null=True, storage=members.models.OverwriteStorage(), upload_to=members.models.user_avatar_path, width_field=b'img_width'),
        ),
    ]