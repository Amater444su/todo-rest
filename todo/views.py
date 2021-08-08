import ipdb
import datetime
import pytz
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
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
from todo.permissions import IsObjectAuthorOrReadOnlyPermission, UserInGroup, IsGroupAdmin


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
    # permission_classes = [UserInGroup]

    def get_queryset(self):
        try:
            queryset = Groups.objects.filter(Q(admin=self.request.user) | Q(users=self.request.user)).distinct()
        except TypeError:
            return None

        return queryset


class GroupsDetailView(generics.RetrieveAPIView):
    """Detail group for admin and members"""
    serializer_class = GroupsSerializer
    permission_classes = [UserInGroup]
    queryset = Groups.objects.all()


class AddUserToGroupView(APIView):
    """Add members to the group"""
    def get(self, request, pk):
        try:
            username_param = self.request.query_params['username']
        except MultiValueDictKeyError:
            username_param = None

        if username_param:
            user = Profile.objects.filter(username=username_param).first()
            group = Groups.objects.filter(id=self.kwargs['pk']).first()
            group.users.add(user)
            return Response(f'User {user.username} was invited')
        return HttpResponse('')


class GroupsDeleteUsersView(APIView):
    """Remove user from the group"""
    permission_classes = (IsGroupAdmin, )

    def get(self, request, user_id, group_id):
        admin = self.request.user
        group = Groups.objects.filter(id=group_id).first()
        user = Profile.objects.filter(id=user_id).first()
        if admin == group.admin:
            group.users.remove(user)
            group.save()
            return Response(f'User {user.username} was removed')
        return Response(f'if ne otrabotal')


class GroupTaskCreateView(generics.CreateAPIView):
    """Create task for current group"""
    queryset = GroupTask
    serializer_class = GroupTaskSerializer
    permission_classes = [UserInGroup]

    def perform_create(self, serializer, **kwargs):
        """Create task and relate this task to group"""
        user = self.request.user
        serializer.save(creator=user)
        group = Groups.objects.filter(id=self.kwargs['group_id']).first()
        task = GroupTask.objects.filter(creator=self.request.user).last()
        group.group_tasks.add(task)
        return Response("Task successfully added")


class GroupTaskListView(generics.ListAPIView):
    """display a List of all tasks in current group"""
    permission_classes = [UserInGroup]
    serializer_class = GroupTaskSerializer

    def get_queryset(self):
        group = Groups.objects.filter(id=self.kwargs['group_id']).first()
        queryset = group.group_tasks.all().order_by('-worker')
        return queryset


# TODO: change naming;
class GroupTaskSetWorkerView(generics.RetrieveAPIView):
    """Makes user the worker of the task"""
    serializer_class = GroupTaskSerializer
    queryset = GroupTask.objects.all()
    # TODO: remove the logic of asign worker to separate method retrieve
    def get_object(self):
        user = self.request.user
        group = Groups.objects.filter(id=self.kwargs['group_id']).first()
        task = group.group_tasks.filter(id=self.kwargs['pk']).first()
        if user not in group.users.all() and user != group.admin:
            raise PermissionDenied
        elif user == task.worker:
            return task
        time_now = datetime.datetime.now()
        # TODO: get deadline from the request
        time_end = time_now + datetime.timedelta(days=3)
        # TODO: change in process into variable
        task.worker, task.status, task.deadline = user, 'In process', time_end
        task.save()
        return task


class GroupTaskEndView(generics.RetrieveAPIView):
    """User's ability to complete a task"""
    queryset = Groups
    serializer_class = GroupTaskSerializer

    def get_object(self):
        user = self.request.user
        group = Groups.objects.filter(id=self.kwargs['group_id']).first()
        task = group.group_tasks.filter(id=self.kwargs['pk']).first()
        if user not in group.users.all() and user != group.admin:
            raise PermissionDenied
        time_now = datetime.datetime.now()
        # TODO: change the replace find another way to compare
        start_task_time = time_now.replace(tzinfo=pytz.utc)
        end_task_time = task.deadline.replace(tzinfo=pytz.utc)
        if start_task_time <= end_task_time:
            task.status = 'Done'
        else:
            task.status = 'Out of date'
        task.save()
        return task


def send_mail_to_worker(request):

    send_mail(
        'Task remain',
        '1 day left before closing your task' + task.task_title,
        'l792899@gmail.com',
        [str(user.email)],
        fail_silently=True
    )
    return 'qwe'


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
