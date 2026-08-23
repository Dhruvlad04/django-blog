from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    # Fields shown in the admin post list
    list_display = [
        "id",
        "title",
        "author",
        "published",
        "created_at"
    ]

    # Fields available for filtering
    list_filter = [
        "published",
        "created_at"
    ]

    # Search by these fields
    search_fields = [
        "title",
        "content",
        "author"
    ]