from django.contrib import admin
from .models import Board, Thread, Post

class PostAdmin(admin.ModelAdmin):
    readonly_fields = (
    	'content',
    	'post_user',
    	'parent_thread',
    	'created'
    )
    list_display = (
    	'post_user',
    	'content',
    	'created'
    )

class ThreadAdmin(admin.ModelAdmin):
	readonly_fields = (
		'title',
		'content',
		'thread_user',
		'parent_board',
		'created'
	)
	list_display = (
		'title',
		'parent_board'
	)

class BoardAdmin(admin.ModelAdmin):
	list_display = (
		'category',
		'description'
	)

admin.site.register(Board, BoardAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)