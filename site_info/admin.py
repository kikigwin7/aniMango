from django import forms
from django.contrib import admin, messages

from tinymce.widgets import TinyMCE

from .models import Exec, HistoryEntry

class ExecForm(forms.ModelForm):
	exec_info = forms.CharField(widget=TinyMCE())

class ExecAdmin(admin.ModelAdmin):
	form = ExecForm
	
	def save_model(self, request, obj, form, change):
		if change:
			old_obj = Exec.objects.get(pk=obj.pk)
			if (not old_obj.academic_year == obj.academic_year) or (not old_obj.user == obj.user):
				messages.add_message(request, messages.ERROR,'Academic year and user entries cannot be modified.')
				return
			if not (request.user == old_obj.user or request.user.member.is_privileged()):
				messages.add_message(request, messages.ERROR,'Exec entries may be changed only by corresponding exec or president/webmaster.')
				return
		super(ExecAdmin, self).save_model(request, obj, form, change)

class HistoryForm(forms.ModelForm):
	body = forms.CharField(widget=TinyMCE())

class HistoryAdmin(admin.ModelAdmin):
	form = HistoryForm

admin.site.register(HistoryEntry, HistoryAdmin)
admin.site.register(Exec, ExecAdmin)



#Don't know where alse to put this -Sorc

#https://stackoverflow.com/questions/2240593/can-django-admin-log-be-monitored-through-djangos-admin
from django.contrib.admin.models import LogEntry
class LogAdmin(admin.ModelAdmin):
	"""Create an admin view of the history/log table"""
	list_display = ('action_time','user','content_type','change_message','is_addition','is_change','is_deletion')
	list_filter = ['action_time','content_type']
	ordering = ('-action_time',)
	readonly_fields = [ 'user','content_type','object_id','object_repr','action_flag','change_message']
	#We don't want people changing this historical record:
	def has_add_permission(self, request):
		return False
	def has_change_permission(self, request, obj=None):
		#returning false causes table to not show up in admin page :-(
		#I guess we have to allow changing for now
		return True
	def has_delete_permission(self, request, obj=None):
		return False
admin.site.register(LogEntry, LogAdmin)