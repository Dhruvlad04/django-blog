from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny

from .models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import PostFilter


class PostViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer

    # Use session login from Django/DRF
    authentication_classes = [
        SessionAuthentication
    ]

    # Our permission controls reading and modifying
    permission_classes = [
        IsOwnerOrReadOnly
    ]

    filterset_class = PostFilter

    search_fields = [
        "title",
        "content"
    ]

    ordering_fields = [
        "title",
        "created_at"
    ]

    # Return all posts.
    # Permission decides who can modify them.
    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")

    # Automatically save the logged-in user as author
    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user
        )