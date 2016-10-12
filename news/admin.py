from django.contrib import admin
from .models import Article
from django.utils import timezone
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
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
	# https://github.com/pydanny-archive/django-wysiwyg#within-django-admin
	# Special template for use with teh wysiwyg editor
	change_form_template = 'news/admin/change_form.html'

	def save_model(self, request, obj, form, change):
		# Override form save, to post user and current time
		obj.created = timezone.localtime(timezone.now())
		obj.created_by = request.user.member
		super(ArticleAdmin, self).save_model(request, obj, form, change)

admin.site.register(Article, ArticleAdmin)