from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    class Meta:
        filter_horizontal = ("replies",)
        list_display = ("author", "message", "reply_to")
        search_fields = ("author", "message", "reply_to")
