from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        # Anyone can read the blog post
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        # Only the author can change or delete the post
        if request.user.is_authenticated:
            return obj.author == request.user.username

        return False