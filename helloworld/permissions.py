from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        # Anyone can read
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Login required for creating/changing/deleting
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Anyone can read
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Only the owner can change or delete
        return obj.author == request.user