from django.db import models
from members.models import Member
from django.utils import timezone
from django.utils.text import slugify
import bleach

# html sanitize whitelist
tags = bleach.ALLOWED_TAGS
tags.extend(['img', 'span', 'br',])
attrs = bleach.ALLOWED_ATTRIBUTES
attrs.update({
	'*': ['style'],
	'img': ['src', 'alt', 'title', 'align'],
})
styles = [
	'color',
	'background-color',
	'text-decoration',
	'font-family',
	'width',
	'height'
]

class Article(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	created = models.DateTimeField()
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
		Member,
		on_delete=models.SET_NULL,
		null=True
	)

	def __str__(self):
		return self.title
	
	def info(self):
		out = 'Category: ' + self.article_type
		out += ', Posted by ' + str(self.created_by)
		return out + ' on ' + self.created.strftime('%d %b %Y')

	def save(self):
		self.content = bleach.clean(
			self.content,
			tags=tags,
			attributes=attrs,
			styles=styles,
		)
		self.slug = slugify(self.title)
		super(Article, self).save()