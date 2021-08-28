import ipdb
from django.urls import reverse
import pytest
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from django.test import RequestFactory
from todo.models import Profile, Todo
from todo.views import TodoDetailView


@pytest.mark.django_db
class TestViews:

    def test_todo_create(self, api_client_authenticated, create_user, user_factory):
        assert Todo.objects.count() == 0
        user = create_user(username='test_user', email='qwe@gmad.com')
        path = reverse('todo-create')

        request_data = {
                'title': 'test_title',
                'description': 'test_description',
                'author': user.id
            }
        # ipdb.set_trace()
        response = api_client_authenticated.post(path, request_data)

        assert response.status_code == 200
        assert Todo.objects.count() == 1

    def test_todo_detail_authenticated(self):
        mixer.blend('todo.Todo')
        path = reverse('todo-edit', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(Profile)

        response = TodoDetailView.as_view()(request, pk=1)
        assert response.status_code == 200

    def test_todo_detail_unauthenticated(self):
        mixer.blend('todo.Todo')
        path = reverse('todo-edit', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = TodoDetailView.as_view()(request, pk=1)
        assert response.status_code == 200

    def test_list_todo(self, create_user, api_client):
        assert Todo.objects.count() == 0
        user = Profile.objects.create(username='test_user', email='foo@bar.com')
        todo = Todo.objects.create(
            title='test_todo',
            author=user,
        )
        response = api_client.get('')

        assert response.status_code == 200
        assert response.json() == [
            {
                'id': todo.id,
                'title': 'test_todo',
                'author': user.id,
                'description': None,
                'categories': None,
                'todo_comment': []
            }
        ]
