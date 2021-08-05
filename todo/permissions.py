from rest_framework.permissions import BasePermission, SAFE_METHODS
from todo.models import Profile


class IsObjectAuthorOrReadOnlyPermission(BasePermission):
    """Check users permission to make edit or Safe methods"""
    message = 'Editing posts is restricted to the author only.'   # Сообщение которое получает Юзер при ошибке
    # То есть если у него не достаточно прав для каких то действий.

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:   # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            # Check permissions for read-only request
            return True
        # else:
        # Check permission for write request
        return obj.author == request.user


class UserInGroupOr403(BasePermission):
    """Check users permission for write and read in groups"""
    def has_object_permission(self, request, view, obj):

        if request.user in obj.users.all() or request.user == obj.admin:
            return True

        return False
