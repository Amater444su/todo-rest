import ipdb
from django import urls
import pytest
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from django.test import RequestFactory
from todo.models import Profile, Todo
from todo.views import TodoDetailView


@pytest.mark.django_db
class TestViews:

    @pytest.mark.parametrize('param', [
        'todo'
    ])
    def test_render_views(self, param, client):
        # client (instance django test client) can simulate post and get requests
        temp_url = urls.reverse(param)
        response = client.get(temp_url)
        assert response.status_code == 200

    def test_todo_create(self, client, create_user):
        assert Todo.objects.count() == 0
        user = create_user(email='foo@bar.com', password='bar', username='test_user')
        response = client.post(
            "/todo-create",
            {
                'title': 'test_title',
                'description': 'test_description',
                'author': user

            }
        )
        assert Todo.objects.count() == 1

    def test_todo_detail_authenticated(self):
        mixer.blend('todo.Todo')
        path = urls.reverse('todo-edit', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(Profile)

        response = TodoDetailView.as_view()(request, pk=1)
        assert response.status_code == 200

    def test_todo_detail_unauthenticated(self):
        mixer.blend('todo.Todo')
        path = urls.reverse('todo-edit', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = TodoDetailView.as_view()(request, pk=1)
        assert response.status_code == 200

    def test_list_todo(self, create_user, client):
        assert Todo.objects.count() == 0
        user = Profile.objects.create(username='test_user', email='foo@bar.com')
        todo = Todo.objects.create(
            title='test_todo',
            author=user,
        )
        response = client.get('')

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
