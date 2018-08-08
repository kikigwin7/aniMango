from django.contrib import admin

from .models import Showing, Show


# Register your models here.

class ShowInline(admin.StackedInline):
    model = Show
    extra = 2
    raw_id_fields = ('lib_series',)


class ShowingAdmin(admin.ModelAdmin):
    inlines = [ShowInline]
    list_filter = [
        'showing_type',
    ]


# Shouldn't register the show model as it complicates things in the admin
admin.site.register(Showing, ShowingAdmin)
