from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post

        fields = [
            "id",
            "title",
            "content",
            "author",
            "created_at",
            "published"
        ]

        # These values are created automatically
        read_only_fields = [
            "id",
            "created_at"
        ]