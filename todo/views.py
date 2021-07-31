import ipdb
from rest_framework import generics
from .models import Todo
from rest_framework import viewsets, permissions
from .serializers import TodoSerializer, TodoDetailSerializer, TodoCreateSerializer


class TodoView(generics.ListAPIView):
    """List View for Todos model"""
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoCreate(generics.CreateAPIView):
    """Create todos"""
    queryset = Todo.objects.all()
    serializer_class = TodoCreateSerializer

    def perform_create(self, serializer):
        #   perform_create(self, serializer)- Вызывается CreateModelMixin при сохранении нового экземпляра объекта.
        serializer.save(author=self.request.user)


class TodoDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    """Read-Write-Delete Todos Detail """
    queryset = Todo.objects.all()
    permission_classes = [PostUserWritePermission]
    serializer_class = TodoDetailSerializer


""" Concrete View Classes
# read = detail, create = create, write = (update/create), update = update, delete = delete.

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
