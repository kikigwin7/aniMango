from django.contrib import admin

from .models import Song, Request, ArchivedRequest


class RequestAdmin(admin.ModelAdmin):
    readonly_fields = (
        'ultrastar_url',
    )

    list_display = (
        'title',
        'artist',
        'ultrastar_url'
    )

    actions = (
        'complete',
        'cancel'
    )

    def complete(self, request, queryset):
        for request_obj in queryset:
            request_obj.complete()

    complete.short_description = "Complete the request"

    def cancel(self, request, queryset):
        for request_obj in queryset:
            request_obj.remove()

    cancel.short_description = "Cancel the request"


admin.site.register(Song)
admin.site.register(Request, RequestAdmin)
admin.site.register(ArchivedRequest)
