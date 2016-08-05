from django.contrib import admin
# Import the series model
from .models import Series

# Class to define custom admin views for the series model
# Makes some fields readonly so the api is used properly
class SeriesAdmin(admin.ModelAdmin):
	readonly_fields = (
		'name',
		'cover_link',
		'synopsis',
		'ani_link',
	)
# Register model with admin site
admin.site.register(Series, SeriesAdmin)