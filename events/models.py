from django.db import models
from members.models import Member

# Create your models here.

class Event(models.Model):
	title = models.CharField(max_length=150)
	when = models.DateTimeField()
	where = models.CharField(max_length=100)
	details = models.TextField()
	max_signups = models.IntegerField(
		help_text='Set to -1 if signup is not required'
	)
	signups_open = models.DateTimeField()
	signups_close = models.DateTimeField()

	def __str__(self):
		return self.title + ' : ' + str(self.when)

class Signup(models.Model):
	who = models.ForeignKey(Member)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	comment = models.CharField(max_length=200)
	created = models.DateTimeField()

	def __str__(self):
		return str(self.who) + ' signup for ' + str(self.event)