# Generated by Django 2.2.12 on 2020-04-21 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karaoke', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='ultrastar_url',
            field=models.URLField(unique=True),
        ),
    ]