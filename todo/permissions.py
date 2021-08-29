import ipdb
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission, SAFE_METHODS
from todo.models import Profile, Groups, Todo


class IsObjectAuthor(BasePermission):
    """Check users permission to make edit or Safe methods"""
    message = 'Editing posts is restricted to the author only.'   # Сообщение которое получает Юзер при ошибке
    # То есть если у него не достаточно прав для каких то действий.

    def has_permission(self, request, view):
        task_id = view.kwargs['pk']
        task = Todo.objects.filter(id=task_id).first()
        return task.author == request.user


class IsGroupAdmin(BasePermission):
    """Check users permission for write and read in groups"""
    def has_permission(self, request, view):
        current_user = request.user
        group = Groups.objects.filter(pk=view.kwargs['group_id']).first()
        if current_user == group.admin:
            return True

        return False


class UserInGroupOrAdmin(BasePermission):
    """Check users permission for write and read in groups"""
    def has_permission(self, request, view):
        current_user = request.user
        group = Groups.objects.filter(pk=view.kwargs['group_id']).first()
        if current_user in group.users.all() or current_user == group.admin:
            return True

        return False


class UserWorkerInGroup(BasePermission):
    """Check users permission for end the task"""

    def has_permission(self, request, view):
        current_user = request.user
        group = Groups.objects.filter(pk=view.kwargs['group_id']).first()
        task = group.group_tasks.filter(id=view.kwargs['pk']).first()
        if current_user == task.worker:
            return True

        return False
