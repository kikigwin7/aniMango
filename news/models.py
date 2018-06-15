from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from aniMango.bleach_html import bleach_tinymce, bleach_no_tags
from members.models import Member

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
		super(Article, self).save()