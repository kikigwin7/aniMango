from django import forms
from django.contrib import admin, messages
from django.contrib.admin.helpers import ActionForm
from django.contrib.auth.models import User

from .models import Item, Series, Request, ArchivedRequest

class ItemInline(admin.StackedInline):
    model = Item
    extra = 1
    raw_id_fields=('parent_series',)

class SeriesAPIForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'

class SeriesAdmin(admin.ModelAdmin):
    actions = None
    form = SeriesAPIForm
    search_fields = ['title', 'title_eng']
    inlines = [ItemInline]
    list_display = (
		'title',
		'series_type',
		'api_id',
		'cooldown_date'
	)
    list_filter = [
        'series_type',
    ]

class CreateLoanForm(ActionForm):
    university_id = forms.CharField()

class ItemAdmin(admin.ModelAdmin):
    raw_id_fields=('parent_series',)
    # What to show as column headers in the admin
    list_display = (
        'name',
        'media_type',
        'parent_series',
        'status',
    )
    list_filter = [
        'media_type',
    ]
    search_fields = ['parent_series']
    action_form = CreateLoanForm
    actions = ['manual_request']
    
    def manual_request(self, request, queryset):
        university_id = request.POST.get('university_id')
        if not university_id:
            self.message_user(request, 'Please provide the university ID', messages.ERROR)
            return
        user = User.objects.get(username=university_id)
        if user:
            for item in queryset:
                r = item.request(user)
                if r:
                    r.approve()
                    self.message_user(request, 'Successfully approved loan for {0!s}'.format(item.__str__()), messages.SUCCESS)
                else:
                    self.message_user(request, 'Could not issue loan for {0!s}'.format(item.__str__()), messages.ERROR)
        else:
            self.message_user(request, 'User {0!s} could not be found'.format(university_id), messages.ERROR)
    manual_request.short_description = "Issue loan to user manually."
    
class RequestAdmin(admin.ModelAdmin):
    readonly_fields = (
        'item',
        'date_requested',
        'status_variable',
        'user'
    )
    # What to show as column headers in the admin
    list_display = (
        'item',
        'status_variable',
        'return_deadline',
        'user',
    )
    list_filter = [
        'status_variable',
    ]
    search_fields = ['item']
    actions = [
        'approve',
        'deny',
        'absent',
        'return_on_time',
        'return_late',
        'renew',
    ]
    
    def approve(self, request, queryset):
        for request_obj in queryset:
            if request_obj.approve():
                messages.add_message(request, messages.SUCCESS, 'Successfully approved loan for {0!s}'.format(request_obj.item.__str__()))
            else:
                messages.add_message(request, messages.ERROR, 'Could not approve loan for {0!s}'.format(request_obj.item.__str__()))
    approve.short_description = "Approve loan request for selected item"
    
    def deny(self, request, queryset):
        for request_obj in queryset:
            if request_obj.deny():
                messages.add_message(request, messages.SUCCESS, 'Successfully denied loan for {0!s}'.format(request_obj.item.__str__()))
            else:
                messages.add_message(request, messages.ERROR, 'Could not deny loan for {0!s}'.format(request_obj.item.__str__()))
    deny.short_description = "Deny loan request for selected items"
    
    def absent(self, request, queryset):
        for request_obj in queryset:
            if request_obj.absent():
                messages.add_message(request, messages.SUCCESS,'Marked as available {0!s}'.format(request_obj.item.__str__()))
            else:
                messages.add_message(request, messages.ERROR,'Could not mark as available {0!s}'.format(request_obj.item.__str__()))
    absent.short_description = "Mark item as not taken due to user being absent"
    
    def return_on_time(self, request, queryset):
        for request_obj in queryset:
            if request_obj.returned('Returned'):
                messages.add_message(request, messages.SUCCESS, 'On time return of {0!s}'.format(request_obj.item.__str__()))
            else:
                messages.add_message(request, messages.ERROR, 'Could not return {0!s}'.format(request_obj.item.__str__()))
    return_on_time.short_description = "Mark items as returned on time"
    
    def return_late(self, request, queryset):
        for request_obj in queryset:
            if request_obj.returned('Late'):
                messages.add_message(request, messages.SUCCESS, 'Late return of {0!s}'.format(request_obj.item.__str__()))
            else:
                messages.add_message(request, messages.ERROR, 'Could not return {0!s}'.format(request_obj.item.__str__()))
    return_late.short_description = "Mark items as returned late"
    
    def renew(self, request, queryset):
        for request_obj in queryset:
            request_obj.renew()
    renew.short_description = "Renew the selected items for one week"
    
class ArchivedRequestAdmin(admin.ModelAdmin):
    readonly_fields = (
        'item',
        'date_requested',
        'date_finalised',
        'return_deadline',
        'status',
        'user',
    )
    # What to show as column headers in the admin
    list_display = (
        'item',
        'status',
        'date_requested',
        'date_finalised',
        'user',
    )
    list_filter = [
        'status',
    ]
    search_fields = ['item']

# Register model with admin site
admin.site.register(Series, SeriesAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(ArchivedRequest, ArchivedRequestAdmin)