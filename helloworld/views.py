from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import PostFilter


class PostViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer

    # User must be logged in
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    filterset_class = PostFilter

    # Used for search
    search_fields = [
        "title",
        "content"
    ]

    # Used for ordering
    ordering_fields = [
        "title",
        "created_at"
    ]

    def get_queryset(self):

        # Only return posts belonging to logged-in user
        return Post.objects.filter(
            author=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):

        # Automatically make logged-in user the author
        serializer.save(
            author=self.request.user
        )