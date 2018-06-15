from django import forms
from django.contrib import admin, messages
from django.utils import timezone

from tinymce.widgets import TinyMCE

from .models import Article

# Register your models here.
class ArticleForm(forms.ModelForm):
	content = forms.CharField(widget=TinyMCE())

class ArticleAdmin(admin.ModelAdmin):
	form = ArticleForm
	
	readonly_fields = (
		'created',
		'created_by',
	)
	list_display = (
		'title',
		'created',
		'created_by',
		'article_type'
	)
	list_filter = [
		'article_type',
	]

	def save_model(self, request, obj, form, change):
		# Override form save, to post user and current time
		if change:
			if not (request.user == obj.created_by or request.user.member.is_privileged()):
				messages.add_message(request, messages.ERROR,'To change an article, you have to be its creator or president/webmaster.')
				return
		else:
			obj.created = timezone.now()
			obj.created_by = request.user

		super(ArticleAdmin, self).save_model(request, obj, form, change)

admin.site.register(Article, ArticleAdmin)