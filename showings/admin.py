from django.contrib import admin

from .models import Showing, Show
# Register your models here.

class ShowInline(admin.StackedInline):
	model = Show
	extra = 1
	readonly_fields = (
        'title',
        'title_eng',
        'ani_link',
        'lib_series'
    )

class ShowingAdmin(admin.ModelAdmin):
	inlines = [ShowInline]

# Shouldn't register the show model as it complicates things in the admin
admin.site.register(Showing, ShowingAdmin)