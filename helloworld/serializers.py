from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):

    # Show the username instead of the complete User object
    author = serializers.ReadOnlyField(
        source="author.username"
    )

    class Meta:
        model = Post

        fields = [
            "id",
            "title",
            "content",
            "author",
            "created_at",
            "updated_at",
            "published"
        ]

        # These values are created automatically
        read_only_fields = [
            "id",
            "author",
            "created_at",
            "updated_at"
        ]