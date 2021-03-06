# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 23:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0005_auto_20161010_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('article_type', models.CharField(choices=[('News', 'News'), ('Minutes', 'Minutes'), ('Blog', 'Blog')], default='News', max_length=8)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.Member')),
            ],
        ),
    ]
