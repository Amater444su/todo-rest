from rest_framework import generics
from .models import Todo
from rest_framework import viewsets, permissions
from .serializers import TodoSerializer, TodoDetailSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS, DjangoModelPermissions


class PostUserWritePermission(BasePermission):
    """Make user permission to create and
    delete stuff"""
    message = 'Editing posts is restricted to the author only.' # Сообщение которое получает Юзер при ошибке
    # То есть если у него не достаточно прав для каких то действий.

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:   # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            # Check permissions for read-only request
            return True
        else:
            # Check permission for write request
            pass
        return obj.author == request.user


class TodoViewSet(viewsets.ModelViewSet):
    """List View for Todos model"""
    queryset = Todo.objects.all()
    permission_classes = [DjangoModelPermissions]   # Permission который указан в settings.py :)
    serializer_class = TodoSerializer


class TodoDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    """Read-Write-Delete Todos Detail """
    queryset = Todo.objects.all()
    permission_classes = [PostUserWritePermission]
    serializer_class = TodoDetailSerializer


""" Concrete View Classes
# read = detail, create = create, write = ?, update = update, delete = delete.
#CreateAPIView
    Used for create-only endpoints.
#ListAPIView
    Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
    Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
    Used for delete-only endpoints for a single model instance.
#UpdateAPIView
    Used for update-only endpoints for a single model instance.
#ListCreateAPIView
    Used for read-write endpoints to represent a collection of model instances.
#RetrieveUpdateAPIView
    Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
    Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
    Used for read-write-delete endpoints to represent a single model instance.
"""
