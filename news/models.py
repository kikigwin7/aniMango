import html
import json
import re
import requests
from django.conf import settings
from django.db import models
from django.utils.text import slugify

from aniMango.bleach_html import bleach_tinymce, bleach_no_tags
from members.models import Member
from .news_config import discordwebhook


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, editable=False)
    article_choices = (
        ('News', 'News'),
        ('Minutes', 'Minutes'),
        ('Blog', 'Blog')
    )
    article_type = models.CharField(
        max_length=8,
        choices=article_choices,
        default='News'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=False
    )

    def __str__(self):
        return self.title

    def info(self):
        out = 'Category: ' + self.article_type
        out += ', Posted by ' + str(self.created_by.member)
        return out + ' on ' + self.created.strftime('%d %b %Y')

    def save(self, **kwargs):
        self.title = bleach_no_tags(self.title)
        self.content = bleach_tinymce(self.content)
        self.slug = slugify(self.title)

        # Begin the webhook to Discord server
        # Note for some god damn stupid reason markupbase is required but doesn't exist anywhere for Python 3.5
        # To make this work, go to https://raw.githubusercontent.com/enthought/Python-2.7.3/master/Lib/markupbase.py
        # and add this to your project site-packages folder
        data = {"username": "Announcements", "embeds": [{
            "title": re.compile(r'<.*?>').sub('', self.title),
            "description": "Created by " + self.created_by.member.nick,
            "url": "http://animesoc.co.uk/news/All/1/",
            "timestamp": self.created.utcnow().isoformat(),
            "fields": [{"name": "Info:", "value": html.unescape(re.sub(re.compile('<.*?>'), '', self.content))}]
        }]
                }
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        response = requests.post(discordwebhook, data=data_json, headers=headers)
        super(Article, self).save()
