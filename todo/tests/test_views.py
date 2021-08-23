import ipdb
from django import urls
from django.contrib.auth import get_user_model
import pytest
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from django.test import RequestFactory
from todo.models import Profile
from todo.views import TodoDetailView


@pytest.mark.django_db
class TestViews:

    @pytest.mark.parametrize('param', [
        ('todo')
    ])
    def test_render_views(self, param, client):
        # client (instance django test client) can simulate post and get requests
        temp_url = urls.reverse(param)
        response = client.get(temp_url)
        assert response.status_code == 200

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
