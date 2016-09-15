from django.contrib import admin
from django.conf.urls import url
from datetime import date, timedelta

from .models import Item, Series

admin.site.disable_action('delete_selected')

class SeriesAdmin(admin.ModelAdmin):
    readonly_fields = (
        'name',
        'cover_link',
        'synopsis',
        'ani_link'
    )
    search_fields = ['name']

# Approve item loan request method
def approve_req(modeladmin, request, queryset):
    for item in queryset:
        if item.status() != 'Requested':
            pass
        else:
            item.requested = False
            item.on_loan = True
            # return date in two weeks time
            item.return_date = date.today() + timedelta(weeks=2)
            item.save()
approve_req.short_description = "Approve loan request for selected item"

# Deny item loan request method
def deny_req(modeladmin, request, queryset):
    for item in queryset:
        if item.status() != 'Requested':
            pass
        else:
            item.requested = False
            item.loan_user = None
            item.save()
deny_req.short_description = "Deny loan request for selected items"

# Recieve an item after or during its loan period
def recieve_loan(modeladmin, request, queryset):
    for item in queryset:
        status = item.status()
        if status == 'On Loan' or status == 'Late':
            item.on_loan = False
            item.loan_user = None
            item.return_date = None
            item.save()
        else:
            pass
recieve_loan.short_description = "Return the items to the library"

# Renew an items loan period
def renew_loan(modeladmin, request, queryset):
    for item in queryset:
        status = item.status()
        if status == 'On Loan' or status == 'Late':
            item.return_date = date.today() + timedelta(weeks=1)
            item.save()
        else:
            pass
renew_loan.short_description = "Renew the the selected items for one week"

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = (
        'on_loan',
        'requested',
        'loan_user',
        'return_date'
    )
    # What to show as column headers in the admin
    list_display = (
        'name',
        'parent_series',
        'status',
        'loan_user',
        'return_date',
    )
    # Fields to filter by on the admin
    list_filter = [
        'requested',
        'on_loan'
    ]
    search_fields = ['parent_series']
    # Add item actions
    actions = [
        approve_req,
        deny_req,
        recieve_loan,
        renew_loan
    ]

# Register model with admin site
admin.site.register(Series, SeriesAdmin)
admin.site.register(Item, ItemAdmin)