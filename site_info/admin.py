from django.contrib import admin
from django import forms
from django.forms import Select

from .models import HistoryEntry, Exec

class HistoryForm(forms.ModelForm):
	class Meta:
		fields = '__all__'
		model = HistoryEntry
		# Overrides the widget so the academic year select is not a huge list
		# Only seems to work if size > 1
		# Don't know why, looking in source, it's undefined behviour lol
		# https://docs.djangoproject.com/en/1.10/_modules/django/forms/widgets/#Select
		widgets = {
			'academic_year': forms.Select(attrs={'size': 2})
		}

class HistoryAdmin(admin.ModelAdmin):
	form = HistoryForm

	# https://github.com/pydanny-archive/django-wysiwyg#within-django-admin
	# Special template for use with teh wysiwyg editor
	change_form_template = 'site_info/admin/change_form.html'


admin.site.register(HistoryEntry, HistoryAdmin)
admin.site.register(Exec)