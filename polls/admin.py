from django.contrib import admin

from .models import Poll, Option


# Register your models here.

class ShowInline(admin.StackedInline):
    model = Option
    extra = 2
    raw_id_fields = ('lib_series',)


class PollAdmin(admin.ModelAdmin):
    inlines = [ShowInline]


# Shouldn't register the show model as it complicates things in the admin
admin.site.register(Poll, PollAdmin)
