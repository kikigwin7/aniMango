from django.db import models
from django.conf import settings
import datetime
import django_wysiwyg

# Create your models here.

class Exec(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		limit_choices_to={'is_staff': True}
	)
	exec_role = models.CharField(max_length=100)
	exec_info = models.TextField()

	def __str__(self):
		return self.exec_role + ' - ' + str(self.user.member)

	class Meta:
		verbose_name_plural = 'Exec'

class HistoryEntry(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()

	# A function to enumerate every academic year as a choice (silly hack lol)
	# Choices are list of tuples
	# Outputs: (year/year+1, year/year+1) as tuple of strings
	YEAR_CHOICES = []
	for y in range(1997, (datetime.datetime.now().year+1)):
		out_format = str(y)+'/'+str(y+1)
		out = (out_format, out_format)
		YEAR_CHOICES.append(out)

	academic_year = models.CharField(
		max_length=9,
		choices=YEAR_CHOICES,
		default='year/year'
	)

	def __str__(self):
		return self.academic_year + ' - ' + self.title

	def save(self):
		self.body = django_wysiwyg.sanitize_html(self.body)
		super(HistoryEntry, self).save()

	class Meta:
		verbose_name_plural = 'History Entries'