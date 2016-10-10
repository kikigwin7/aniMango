from django.db import models
from members.models import Member

class Board(models.Model):
	category = models.CharField(max_length=100)
	description = models.CharField(max_length=150)

	def __str__(self):
		return self.category

class Thread(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	thread_user = models.ForeignKey(Member)
	parent_board = models.ForeignKey(Board)
	created = models.DateTimeField()

	def __str__(self):
		return str(self.parent_board) + ' : ' + self.title

	def info(self):
		out = 'Created by ' + str(self.thread_user)
		return out + ' at ' + self.created.strftime('%c')

class Post(models.Model):
	content = models.TextField()
	post_user = models.ForeignKey(Member)
	parent_thread = models.ForeignKey(Thread)
	deleted = models.BooleanField(default=False)
	edited = models.BooleanField(default=False)
	created = models.DateTimeField()

	def __str__(self):
		out = 'Response to: ' + str(self.parent_thread)
		return out + ' - by: ' + str(self.post_user) + ' : ' + self.content

	def by(self):
		out = 'Posted by ' + str(self.post_user)
		return out + ' at ' + self.created.strftime('%c')