from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Meta:
        list_display = ["title", "slug", "author", "published"]
        list_filter = ["author", "published"]
        search_fields = ["title", "content"]
        ordering = ["-published"]