from django.contrib import admin
# Import the models for the library app
from .models import Item, Loan, Series

# Make some fields readonly so the api is used properly
class SeriesAdmin(admin.ModelAdmin):
	readonly_fields = (
		'name',
		'cover_link',
		'synopsis',
		'ani_link'
	)

# Register model with admin site
admin.site.register(Series, SeriesAdmin)
admin.site.register(Item)
admin.site.register(Loan)