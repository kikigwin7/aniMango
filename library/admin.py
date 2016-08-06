from django.contrib import admin
# Import the models for the library app
from .models import Item, Series

# Make some fields readonly so the api is used properly
class SeriesAdmin(admin.ModelAdmin):
	readonly_fields = (
		'name',
		'cover_link',
		'synopsis',
		'ani_link'
	)

class ItemAdmin(admin.ModelAdmin):
	readonly_fields = (
		'on_loan',
		'requested',
		'loan_user',
		'return_date'
	)

# Register model with admin site
admin.site.register(Series, SeriesAdmin)
admin.site.register(Item, ItemAdmin)