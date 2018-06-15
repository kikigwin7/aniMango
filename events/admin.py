from datetime import timedelta

from django import forms
from django.contrib import admin, messages
from django.utils import timezone

from tinymce.widgets import TinyMCE

from .models import Event, Signup

class EventForm(forms.ModelForm):
	
	details = forms.CharField(widget=TinyMCE())

	def clean(self):
		# Call regular clean
		cleaned_data = super(EventForm, self).clean()
		# Get the cleaned data
		event_start = cleaned_data.get('when')
		signup_open = cleaned_data.get('signups_open')
		signup_close = cleaned_data.get('signups_close')

		# If the data are none then they were invalid
		if not event_start or not signup_open or not signup_close:
			raise forms.ValidationError('Please enter a valid date')
		
		if event_start < signup_open:
			raise forms.ValidationError('Signups must open before event start')
		elif signup_open > signup_close:
			raise forms.ValidationError('Signups must open before signups close')

		return cleaned_data

	class Meta:
		model = Event
		fields = '__all__'

class EventAdmin(admin.ModelAdmin):
	form = EventForm
	
	list_display = (
		'title',
		'when',
		'signups_close',
		'where',
		'signup_count'
	)
	
class SignupAdmin(admin.ModelAdmin):
	readonly_fields = (
		'event',
		'who',
		'created',
	)
	
	list_display = (
		'event',
		'who',
		'comment',
		'created',
	)
	
	def save_model(self, request, obj, form, change):
		if change:
			if not (timezone.now() < obj.created + timedelta(days=7) or request.user.member.is_privileged()):
				messages.add_message(request, messages.ERROR,'Signups may be changed only for a week, unless you are president/webmaster.')
				return
		super(SignupAdmin, self).save_model(request, obj, form, change)

admin.site.register(Event, EventAdmin)
admin.site.register(Signup, SignupAdmin)