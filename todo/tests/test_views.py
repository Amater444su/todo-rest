import ipdb
from django.urls import reverse
import pytest
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from django.test import RequestFactory
from rest_framework.test import APIClient
from django.db import transaction

from todo.models import Profile, Todo
from todo.tests.factories import TodoFactory
from todo.views import TodoDetailView


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

    # def test_list_todo(self, api_client_authenticated, user):
    #     assert Todo.objects.count() == 0
    #     todo = Todo.objects.create(
    #         title='test_todo',
    #         author=user,
    #     )
    #     response = api_client_authenticated.get('')
    #
    #     assert response.status_code == 200
    #     assert response.json() == [
    #         {
    #             'id': todo.id,
    #             'title': 'test_todo',
    #             'author': user.id,
    #             'description': None,
    #             'categories': None,
    #             'todo_comment': []
    #         }
    #     ]


class TestGroupView:
    pass
