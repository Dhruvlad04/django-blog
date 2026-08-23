from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import PostFilter


class PostViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer

    authentication_classes = [
        SessionAuthentication
    ]

    permission_classes = [
        IsOwnerOrReadOnly
    ]

    filterset_class = PostFilter

    search_fields = ["title", "content"]

    ordering_fields = ["title", "created_at"]

    def get_queryset(self):
        # Return all posts here so that
        # permission can check the owner.
        return Post.objects.all().order_by("-created_at")

    def list(self, request, *args, **kwargs):
        # For the list page, logged-in users
        # should see only their own posts.

        if request.user.is_authenticated:
            posts = Post.objects.filter(
                author=request.user
            ).order_by("-created_at")
        else:
            # Public users can read posts
            posts = Post.objects.all().order_by("-created_at")

        # Apply filters/search/ordering
        posts = self.filter_queryset(posts)

        page = self.paginate_queryset(posts)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                serializer.data
            )

        serializer = self.get_serializer(
            posts,
            many=True
        )

        return Response(serializer.data)

    def perform_create(self, serializer):
        # Logged-in user becomes the author
        serializer.save(
            author=self.request.user
        )