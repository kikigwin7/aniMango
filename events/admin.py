from django.contrib import admin
from .models import Event, Signup
from django import forms

class EventForm(forms.ModelForm):

	def clean(self):
		# Call regular clean
		cleaned_data = super(EventForm, self).clean()
		# Get the cleaned data
		event_start = cleaned_data.get('when')
		signup_open = cleaned_data.get('signups_open')
		signup_close = cleaned_data.get('signups_close')

		# If the data are non then they were invalid
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

admin.site.register(Event, EventAdmin)
admin.site.register(Signup)