from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly
from .filters import PostFilter
class PostViewSet(viewsets.ModelViewSet):
    # Get all posts from database
    queryset = Post.objects.all().order_by("-created_at")
    # Convert Post objects to JSON
    serializer_class = PostSerializer
    # Apply our permission rules
    permission_classes = [IsAuthorOrReadOnly]
    # Enable filtering
    filterset_class = PostFilter
    # Fields used by the search option
    search_fields = [
        "title",
        "content",
        "author"
    ]
    # Fields that can be used for ordering
    ordering_fields = [
        "title",
        "created_at"
    ]