from rest_framework.permissions import BasePermission, SAFE_METHODS


class PostUserWritePermission(BasePermission):
    """Make user permission to create and
    delete stuff"""
    message = 'Editing posts is restricted to the author only.'   # Сообщение которое получает Юзер при ошибке
    # То есть если у него не достаточно прав для каких то действий.

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:   # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            # Check permissions for read-only request
            return True
        else:
            # Check permission for write request
            pass
        return obj.author == request.user
