from datetime import timedelta

from django.contrib import admin, messages
from .models import Board, Thread, Post
from django.utils import timezone


class PostAdmin(admin.ModelAdmin):
    readonly_fields = (
        'original',
        'post_user',
        'parent_thread',
        'created',
        'edited',
    )
    list_display = (
        'post_user',
        'content',
        'created'
    )
    list_filter = [
        'deleted',
        'edited',
    ]

    def save_model(self, request, obj, form, change):
        if change:
            if not (timezone.now() < obj.created + timedelta(days=4) or request.user.member.is_privileged()):
                messages.add_message(request, messages.ERROR,
                                     'Posts may be changed only for 4 days, unless you are president/webmaster.')
                return
        super(PostAdmin, self).save_model(request, obj, form, change)


class ThreadAdmin(admin.ModelAdmin):
    readonly_fields = (
        'title',
        'thread_user',
        'parent_board',
        'created',
        'last_reply_time',
    )
    list_display = (
        'title',
        'parent_board',
        'thread_user',
    )
    list_filter = [
        'parent_board',
    ]


class BoardAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'description'
    )


admin.site.register(Board, BoardAdmin)
admin.site.register(Thread, ThreadAdmin)
# Uncomment if you need admin for posts, not really needed
# But then how do I moderate? -Sorc
# TODO: I guess writing something simple that works directly on the forum page would be nice -Sorc
admin.site.register(Post, PostAdmin)
