from django.db import models
from django.template.defaultfilters import date as d_date
from django.utils import timezone

from aniMango.bleach_html import bleach_tinymce, bleach_no_tags
from members.models import Member

class Board(models.Model):
	category = models.CharField(max_length=100)
	description = models.CharField(max_length=150)
	order = models.IntegerField()
	locked = models.BooleanField(default=False)

	def __str__(self):
		return self.category

class Thread(models.Model):
	title = models.CharField(max_length=100)
	thread_user = models.ForeignKey(Member, on_delete=models.PROTECT)
	# You would not want to delete a board before moving threads elsewhere, would you? -Sorc
	parent_board = models.ForeignKey(Board, on_delete=models.PROTECT)
	created = models.DateTimeField(null=False, blank=False)
	last_reply_time = models.DateTimeField()
	locked = models.BooleanField(default=False)

	def __str__(self):
		return str(self.parent_board) + ' : ' + self.title

	def save(self):
		self.title = bleach_no_tags(self.title)
		super(Thread, self).save()

	def info(self):
		return 'Created by {0!s} on {1!s}'.format(self.thread_user, d_date(self.created, 'D jS F Y, H:i'))

	def last_reply_info(self):
		return 'Last reply on {0!s}'.format(d_date(self.last_reply_time, 'D jS F Y, H:i'))

	def last_reply_now(self):
		self.last_reply_time = timezone.now()
		self.save()

class Post(models.Model):
	original = models.TextField() #Contains original content, if it was ever modified. - Sorc
	content = models.TextField(blank=False, null=False)
	post_user = models.ForeignKey(Member, on_delete=models.PROTECT)
	parent_thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
	deleted = models.BooleanField(default=False)
	locked = models.BooleanField(default=False)
	edited = models.BooleanField(default=False)
	created = models.DateTimeField()

	def __str__(self):
		out = 'Response to: ' + str(self.parent_thread)
		return 'Reply to {0!s} by {1!s}: {2!s}'.format(self.parent_thread, self.post_user, self.content)

	def by(self):
		return '{0!s} | {1!s}'.format(self.post_user, d_date(self.created, 'D jS F Y, H:i'))

	def save(self):
		self.content = bleach_tinymce(self.content)
		super(Post, self).save()

	def delete(self):
		self.deleted=True
		self.save()

	def edit(self, new_content):
		if self.parent_thread.locked:
			raise Warning('Thread is locked')
		if self.locked:
			raise Warning('Post is locked')
		if not self.original:
			self.original = self.content
		self.content=new_content
		self.edited=True
		self.save()
