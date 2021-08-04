import ipdb
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics, status
from rest_framework.views import APIView
from todo.models import (
    Todo, Comments, Groups, GroupTask, Profile
        )
from rest_framework import viewsets, permissions
from todo.serializers import (
    TodoSerializer, TodoDetailSerializer, TodoCreateSerializer, CommentSerializer,
    GroupsSerializer, GroupTaskSerializer
            )
from todo.permissions import IsObjectAuthorOrReadOnlyPermission


# class Logout(APIView):
#
#     def get(self, request, format=None):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)


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


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Read-Write-Delete Todos Detail """
    queryset = Todo.objects.all()
    permission_class = [IsObjectAuthorOrReadOnlyPermission]
    serializer_class = TodoDetailSerializer


class CommentCreateView(generics.ListCreateAPIView):
    """Create comment for a particular todo"""
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer, **kwargs):
        #   perform_create(self, serializer)- Вызывается CreateModelMixin при сохранении нового экземпляра объекта.
        serializer.save(author=self.request.user, todo_id=self.kwargs.get('todo_id'))


class GroupsCreateView(generics.CreateAPIView):
    """Create group and declare admin"""
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer

    def perform_create(self, serializer, **kwargs):
        serializer.save(admin=self.request.user)


class GroupsView(generics.ListAPIView):
    """List of all groups"""
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer


class GroupsDetailView(generics.RetrieveUpdateAPIView):
    """Detail group for admin and members"""
    serializer_class = GroupsSerializer

    def get_queryset(self):
        # ipdb.set_trace()
        queryset = Groups.objects.all()
        try:
            username_param = self.request.query_params['username']
        except MultiValueDictKeyError:
            username_param = None

        if username_param:
            user = Profile.objects.filter(username=username_param).first()
            group = queryset.filter(id=self.kwargs['pk']).first()
            group.users.add(user)
        else:
            queryset = Groups.objects.all()
        return queryset


class GroupsDeleteUsersView(APIView):
    """Remove user from the group"""
    def get(self, request, user_id):
        admin = self.request.user
        group = Groups.objects.filter(admin=admin).first()
        user = Profile.objects.filter(id=user_id).first()
        group.users.remove(user)
        group.save()
        return HttpResponse('')


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
