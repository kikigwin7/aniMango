from django.contrib import admin
from django import forms
from django.conf.urls import url
from datetime import date, timedelta
from anilist_api.anilist import ANILIST_MAGIC_NUMBER

from .models import Item, Series

class ItemInline(admin.StackedInline):
    model = Item
    extra = 1
    readonly_fields = (
        'on_loan',
        'requested',
        'loan_user',
        'return_date'
    )

class SeriesAPIForm(forms.ModelForm):
    anilist_series_number = forms.IntegerField(
        widget=forms.TextInput,
        required=False
    )

    class Meta:
        model = Series
        fields = '__all__'

class SeriesAdmin(admin.ModelAdmin):
    actions = None
    form = SeriesAPIForm
    readonly_fields = (
        'api_anime',
        'api_manga',
        'title',
        'title_eng',
        'cover_link',
        'synopsis',
        'ani_link'
    )
    search_fields = ['name']
    inlines = [ItemInline]

    def save_model(self, request, obj, form, change):
        # Override form save, to input given series number in the correct field
        series_no = form.cleaned_data['anilist_series_number']
        if series_no is None:
            pass
        elif series_no > ANILIST_MAGIC_NUMBER:
            obj.api_manga = series_no
        else:
            obj.api_anime = series_no

        super(SeriesAdmin, self).save_model(request, obj, form, change)


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
    actions = [
        'approve_req',
        'deny_req',
        'recieve_loan',
        'renew_loan'
    ]

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