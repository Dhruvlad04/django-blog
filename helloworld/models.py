from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    # Blog post title
    title = models.CharField(max_length=200)

    # Blog post content
    content = models.TextField()

    # The post belongs to one Django user
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    # Automatically stores when the post is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically stores when the post is updated
    updated_at = models.DateTimeField(auto_now=True)

    # True means the post is published
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title