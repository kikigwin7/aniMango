from django.db import models
from members.models import Member
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import date as d_date

class Event(models.Model):
	title = models.CharField(max_length=150)
	subtitle = models.CharField(max_length=150)
	when = models.DateTimeField()
	where = models.CharField(max_length=100)
	details = models.TextField()
	max_signups = models.IntegerField(
		help_text='Set to -1 if signup is not required'
	)
	signups_open = models.DateTimeField()
	signups_close = models.DateTimeField()

	def __str__(self):
		out = self.title + ', ' + d_date(self.when, 'D jS F Y, H:i')
		return out + ', ' + self.where

	def week_start(self):
		# Get the day at the start of the week
		return self.when - timedelta(days=self.when.weekday())

	def is_full(self):
		if self.max_signups < 0:
			return False
		elif self.signup_set.count() < self.max_signups:
			return False
		else:
			return True

	def already_signed_up(self, member):
		# Check of member is already signed up
		try:
			self.signup_set.get(who=member)
			return True
		except ObjectDoesNotExist:
			return False

	def signup_count(self):
		# How many people have signed up
		return str(self.signup_set.count()) + '/' + str(self.max_signups)

	def closed(self):
		# Event is closed past signup close
		if self.signups_close > datetime.now():
			return True
		else:
			return False

class Signup(models.Model):
	who = models.ForeignKey(Member)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	comment = models.CharField(max_length=200, blank=True)
	created = models.DateTimeField()

	def __str__(self):
		return str(self.who) + ' signup for ' + str(self.event)