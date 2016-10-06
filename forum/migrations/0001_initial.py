# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-06 14:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0004_auto_20161004_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('deleted', models.BooleanField(default=False)),
                ('edited', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('first', models.BooleanField()),
                ('next_post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='forum.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created', models.DateTimeField()),
                ('parent_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Board')),
                ('thread_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Member')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='parent_thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Thread'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Member'),
        ),
    ]
