import datetime

from django.conf import settings
from django.db import models

from aniMango.bleach_html import bleach_tinymce, bleach_no_tags

def get_year_choices():
	return [(r,r) for r in range(1997, datetime.date.today().year+1)]

class Exec(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,# Make sure deleting history is harder. If needed, just deactivate accounts -Sorc
		limit_choices_to={'is_staff': True}
	)
	exec_role = models.CharField(max_length=100)
	place_in_list = models.IntegerField(default=100);
	exec_info = models.TextField()
	
	academic_year = models.IntegerField(
		"Academic year starting",
		choices=get_year_choices(),
		default=datetime.datetime.now().year
	)

	def __str__(self):
		return '{0!s} - {1!s} ({2!s})'.format(self.academic_year, self.user.member, self.exec_role)
		
	def save(self):
		self.exec_role = bleach_no_tags(self.exec_role)
		self.exec_info = bleach_tinymce(self.exec_info)
		super(Exec, self).save()

	class Meta:
		verbose_name_plural = 'Exec'
		ordering = ['-academic_year', 'place_in_list']

class HistoryEntry(models.Model):
	title = models.CharField(max_length=200)
	body = models.TextField()
	
	academic_year = models.IntegerField(
		"Academic year starting",
		choices=get_year_choices(),
		default=datetime.datetime.now().year
	)

	def __str__(self):
		return '{0!s}/{1!s} - ({2!s})'.format(self.academic_year, self.academic_year+1, self.title)

	def save(self):
		self.title = bleach_no_tags(self.title)
		self.body = bleach_tinymce(self.body)
		super(HistoryEntry, self).save()

	class Meta:
		verbose_name_plural = 'History Entries'
		ordering = ['-academic_year']