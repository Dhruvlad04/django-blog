from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "title",
        "author",
        "published",
        "created_at"
    ]

    list_filter = [
        "published",
        "created_at"
    ]

    search_fields = [
        "title",
        "content",
        "author__username"
    ]