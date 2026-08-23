from django.db import models


class Post(models.Model):
    # Title of the blog post
    title = models.CharField(max_length=200)

    # Main content of the blog
    content = models.TextField()

    # Name of the person who wrote the post
    author = models.CharField(max_length=100)

    # Django automatically stores the creation time
    created_at = models.DateTimeField(auto_now_add=True)

    # This tells whether the post is published or not
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title