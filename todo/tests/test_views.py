import ipdb
from django.urls import reverse
import pytest
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from django.test import RequestFactory
from rest_framework.test import APIClient
from django.db import transaction

from todo.models import Profile, Todo, Comments
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

    def test_list_todo(self, api_client_authenticated, user, todo):
        todo.author = user
        todo.save()
        path = reverse('todo')
        response = api_client_authenticated.get(path)
        # ipdb.set_trace()
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
        # ipdb.set_trace()
        assert response.json() == {

                'id': comment.id,
                'text': comment.text
            }



class TestGroupView:
    pass
