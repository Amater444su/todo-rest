import ipdb
import datetime
import pytz
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
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
from todo.permissions import IsObjectAuthorOrReadOnlyPermission, UserInGroupOr403


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


class GroupListDetailView(generics.ListAPIView):
    """List of all groups available for user"""
    serializer_class = GroupsSerializer
    permission_classes = [UserInGroupOr403]

    def get_queryset(self):
        queryset = Groups.objects.filter(admin=self.request.user) or Groups.objects.filter(users=self.request.user)
        # queryset = Groups.objects.filter(Q(admin=self.request.user) | Q(users=self.request.user))
        return queryset


class GroupsDetailView(generics.RetrieveUpdateAPIView):
    """Detail group for admin and members"""
    serializer_class = GroupsSerializer
    permission_classes = [UserInGroupOr403]

    def get_queryset(self):
        """Add members to the group"""
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
    def get(self, request, user_id, group_id):
        admin = self.request.user
        group = Groups.objects.filter(id=group_id).first()
        user = Profile.objects.filter(id=user_id).first()
        if admin == group.admin:
            group.users.remove(user)
            group.save()
            return HttpResponse('')
        else:
            raise PermissionDenied


class GroupTaskCreateView(generics.CreateAPIView):
    """Create task for current group"""
    queryset = GroupTask
    serializer_class = GroupTaskSerializer

    def perform_create(self, serializer, **kwargs):
        """Create task and relate this task to group"""
        # ipdb.set_trace()
        user = self.request.user
        serializer.save(creator=self.request.user)
        group = Groups.objects.filter(id=self.kwargs['group_id']).first()
        task = GroupTask.objects.filter(creator=self.request.user).last()
        if user in group.users.all():
            group.group_tasks.add(task)
        else:
            task.delete()
            raise PermissionDenied


class GroupTaskListView(generics.ListAPIView):
    """List display for all tasks in current group"""
    # permission_classes = [UserInGroupOr403]
    serializer_class = GroupTaskSerializer

    def get_queryset(self):
        # ipdb.set_trace()
        group = Groups.objects.filter(id=self.kwargs['group_id']).first()
        queryset = group.group_tasks.all().order_by('-worker')
        if self.request.user not in group.users.all():
            raise PermissionDenied
        return queryset


class GroupTaskSetWorkerView(generics.RetrieveAPIView):
    """Make user writer of the task"""
    serializer_class = GroupTaskSerializer
    queryset = GroupTask.objects.all()

    def get_object(self):
        user = self.request.user
        group = Groups.objects.filter(id=self.kwargs['group_id']).first()
        if user not in group.users.all():
            raise PermissionDenied
        task = group.group_tasks.filter(id=self.kwargs['pk']).first()
        time_now = datetime.datetime.now()
        time_end = time_now + datetime.timedelta(days=3)
        task.worker = user
        task.status = 'In process'
        task.deadline = time_end
        task.save()
        return task


class GroupTaskEndView(generics.RetrieveAPIView):
    """Make user to end the task"""
    queryset = GroupTask
    serializer_class = GroupTaskSerializer

    def get_object(self):
        user = self.request.user
        group = Groups.objects.filter(id=self.kwargs['group_id']).first()
        task = group.group_tasks.filter(id=self.kwargs['pk']).first()
        if user not in group.users.all():
            raise PermissionDenied
        time_now = datetime.datetime.now()
        start_time = time_now.replace(tzinfo=pytz.utc)
        end_time = task.deadline.replace(tzinfo=pytz.utc)
        if start_time <= end_time:
            task.status = 'Done'
        else:
            task.status = 'Out of date'
        task.save()
        return task





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
