import ipdb
from django.urls import reverse
import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from rest_framework.test import APIClient
from django.db import transaction

from todo.models import Profile, Todo, Comments, Groups


@pytest.mark.django_db
class TestTodoViews:

    def test_todo_create(self, api_client_authenticated, user):
        assert Todo.objects.count() == 0
        path = reverse('todo-create')
        request_data = {
                'title': 'test_title',
                'description': 'test_description',
                'author': user.id
            }
        response = api_client_authenticated.post(path, request_data)

        assert response.status_code == 201
        assert Todo.objects.count() == 1

    def test_todo_detail_authenticated(self, api_client_authenticated, todo, user):
        todo.author = user
        todo.save()
        path = reverse('todo-edit', kwargs={'pk': todo.id})
        response = api_client_authenticated.get(path)

        assert response.status_code == 200

    def test_todo_detail_unauthenticated(self, todo):
        path = reverse('todo-edit', kwargs={'pk': todo.id})
        client = APIClient()
        response = client.get(path)

        assert response.status_code == 403

    def test_list_todo(self, api_client_authenticated, user, todo):
        todo.author = user
        todo.save()
        path = reverse('todo')
        response = api_client_authenticated.get(path)
        assert response.status_code == 200
        assert Todo.objects.count() == 1
        assert response.json() == [
            {
                'id': todo.id,
                'title': todo.title,
                'author': user.username,
                'description': None,
                'categories': None,
                'todo_comment': []
            }
        ]

    def test_create_comment_for_todo(self, api_client_authenticated, todo):
        assert Comments.objects.count() == 0

        path = reverse('todo-comment', kwargs={'todo_id': todo.id})
        request_data = {
            'text': 'test_text'
        }
        response = api_client_authenticated.post(path, request_data)
        comment = Comments.objects.get(id=1)

        assert response.status_code == 201
        assert Comments.objects.count() == 1
        assert response.json() == {

                'id': comment.id,
                'text': comment.text
            }


@pytest.mark.django_db
class TestGroupView:

    def test_group_create(self, api_client_authenticated):
        assert Groups.objects.count() == 0

        path = reverse('group_create')
        request_data = {
            'name': 'test_group'
        }
        response = api_client_authenticated.post(path, request_data)
        group = Groups.objects.get(id=1)

        assert response.status_code == 201
        assert Groups.objects.count() == 1
        assert response.json() == {
            'id': group.id,
            'name': group.name,
            'admin': group.admin.username,
            'group_tasks': [],
            'users': []

        }

    def test_list_display_all_groups(self, api_client_authenticated):
        path = reverse('group')
        response = api_client_authenticated.get(path)

        assert response.status_code == 200

    def test_detail_group(self, api_client_authenticated, groups, user):
        groups.admin = user
        groups.save()

        path = reverse('group_detail', kwargs={'group_id': groups.id})
        response = api_client_authenticated.get(path)

        assert response.status_code == 200

    def test_add_user_to_group(self, api_client_authenticated, groups, user):
        groups.admin = user
        groups.save()
        path = reverse('group_detail', kwargs={'group_id': groups.id})
        response = api_client_authenticated.get(path)

        assert response.status_code == 200
        assert response.json() == {
            'id': groups.id,
            'name': groups.name,
            'admin': groups.admin.username,
            'group_tasks': [],
            'users': []
        }

        path = reverse('group_add_user', kwargs={'group_id': groups.id})
        response = api_client_authenticated.get(path, {'username': str(user.username)})

        assert response.status_code == 200
        assert response.json() == f'User <{user.username}> was invited'

    def test_list_groups_for_user(self, api_client_authenticated, groups, user):
        groups.admin = user
        groups.save()
        path = reverse('users_group')
        response = api_client_authenticated.get(path)

        assert response.status_code == 200
        assert Groups.objects.count() == 1
        assert response.json() == [
            {
                'id': groups.id,
                'name': groups.name,
                'group_tasks': [],
                'users': [],
                'admin': groups.admin.username
            }
        ]

    def test_group_remove_user(self, api_client_authenticated, groups, user):
        groups.users.add(user)
        path = reverse('group_detail', kwargs={'group_id': groups.id})
        response = api_client_authenticated.get(path)

        assert response.status_code == 200
        assert response.json() == {
            'id': groups.id,
            'name': groups.name,
            'admin': groups.admin.username,
            'group_tasks': [],
            'users': [str(user.username)]
        }

        groups.admin = user
        groups.save()
        path = reverse('group_remove_user', kwargs={'group_id': groups.id, 'user_id': str(user.id)})
        response = api_client_authenticated.get(path)

        assert response.status_code == 200
        assert response.json() == f'User {user.username} was removed'
