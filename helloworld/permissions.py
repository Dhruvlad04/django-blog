from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # Anyone can read posts
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # User must be logged in for changes
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Anyone can view a post
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Only the owner can change or delete the post
        return obj.author == request.user