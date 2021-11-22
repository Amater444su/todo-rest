import ipdb
from datetime import datetime, timedelta
import pytz
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics, status
from rest_framework.views import APIView
from todo.models import (
    Todo, Comments, Groups, GroupTask, Profile,
    GroupTaskStatuses
)
from todo.serializers import (
    TodoSerializer, TodoDetailSerializer, TodoCreateSerializer, CommentSerializer,
    GroupsSerializer, GroupTaskSerializer
)
from todo.permissions import IsObjectAuthor, UserInGroupOrAdmin, IsGroupAdmin, UserWorkerInGroup


class TodoView(generics.ListAPIView):
    """Display all todos"""
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoCreate(generics.CreateAPIView):
    """Create todos"""
    queryset = Todo.objects.all()
    serializer_class = TodoCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Read-Write-Delete Todos Detail """
    queryset = Todo.objects.all()
    permission_classes = (IsObjectAuthor, )
    serializer_class = TodoDetailSerializer


class CommentCreateView(generics.ListCreateAPIView):
    """Create comment for a particular todo"""
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer, **kwargs):
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Groups.objects.filter(Q(admin=self.request.user) | Q(users=self.request.user)).distinct()
        return queryset


class GroupsDetailView(generics.RetrieveAPIView):
    """Detail group for admin and members"""
    serializer_class = GroupsSerializer
    lookup_url_kwarg = 'group_id'
    permission_classes = [UserInGroupOrAdmin]
    queryset = Groups


class AddUserToGroupView(APIView):
    """Add members to the group"""

    def get(self, request, group_id):
        group_id = self.kwargs['group_id']
        try:
            username_param = self.request.query_params['username']
        except MultiValueDictKeyError:
            username_param = None

        if username_param:
            user = Profile.objects.filter(username=username_param).first()
            if not user:
                raise APIException(f'There is no user with such username <{username_param}>')
            group = Groups.objects.filter(id=group_id).first()
            group.users.add(user)
            return Response(f'User <{user.username}> was invited')

        return Response()


class GroupsDeleteUsersView(APIView):
    """Remove user from the group"""
    permission_classes = (IsGroupAdmin,)

    def get(self, request, user_id, group_id):
        admin = self.request.user
        group = Groups.objects.filter(id=group_id).first()
        user = Profile.objects.filter(id=user_id).first()
        if admin == group.admin:
            group.users.remove(user)
            group.save()
            return Response(f'User {user.username} was removed')
        return Response()


class GroupTaskCreateView(generics.CreateAPIView):
    """Create task for current group"""
    queryset = GroupTask
    serializer_class = GroupTaskSerializer
    permission_classes = [UserInGroupOrAdmin]

    def perform_create(self, serializer, **kwargs):
        """Create task and relate this task to group"""
        return serializer.save(creator=self.request.user)


class GroupTaskListView(generics.ListAPIView):
    """display a List of all tasks in current group"""
    permission_classes = [UserInGroupOrAdmin]
    serializer_class = GroupTaskSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group = Groups.objects.filter(id=group_id).first()
        queryset = group.group_tasks.all().order_by('-worker')
        return queryset


class AssignWorkerApiView(APIView):
    """Assign user as the worker of the task"""
    permission_classes = [UserInGroupOrAdmin]

    def get(self, request, pk, group_id):
        current_user = self.request.user
        group = Groups.objects.filter(id=group_id).first()
        task = group.group_tasks.filter(id=pk).first()
        # TODO: get deadline from the request
        deadline = datetime.now() + timedelta(days=3)
        task.worker = current_user
        task.status = GroupTaskStatuses.IN_PROCESS
        task.deadline = deadline
        task.save()
        return Response(f'You are now the worker of <{task.task_title}>')


class GroupTaskEndView(APIView):
    """User's ability to complete a task"""
    permission_classes = [UserInGroupOrAdmin, UserWorkerInGroup]

    def get(self, request, group_id, pk):
        group = Groups.objects.filter(id=group_id).first()
        task = group.group_tasks.filter(id=pk).first()
        time_now = datetime.now()
        # TODO: change the replace find another way to compare
        start_task_time = time_now.replace(tzinfo=pytz.utc)
        end_task_time = task.deadline.replace(tzinfo=pytz.utc)
        if start_task_time <= end_task_time:
            task.status = GroupTaskStatuses.DONE
        else:
            task.status = GroupTaskStatuses.OUT_OF_DATE
        task.save()
        return Response(f'Task successfully submitted as {task.status}')


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
