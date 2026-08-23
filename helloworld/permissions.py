from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        # Allow users to read their own post
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return obj.author == request.user

        # Only the owner can update or delete
        return obj.author == request.user