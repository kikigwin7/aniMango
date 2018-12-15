from django.contrib import admin

from .models import Item


class ArchiveAdmin(admin.ModelAdmin):
    pass


admin.site.register(Item, ArchiveAdmin)
