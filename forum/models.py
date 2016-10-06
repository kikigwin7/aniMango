from django.db import models
from members.models import Member

class Board(models.Model):
	category = models.CharField(max_length=100)

class Thread(models.Model):
	title = models.CharField(max_length=100)
	thread_user = models.ForeignKey(Member)
	parent_board = models.ForeignKey(Board)
	created = models.DateTimeField()

class Post(models.Model):
	content = models.TextField()
	post_user = models.ForeignKey(Member)
	parent_thread = models.ForeignKey(Thread)
	next_post = models.OneToOneField('self')
	deleted = models.BooleanField(default=False)
	edited = models.BooleanField(default=False)
	created = models.DateTimeField()
	first = models.BooleanField()