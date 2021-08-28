import ipdb
import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from pytest_factoryboy import register
from rest_framework.test import APIClient

from todo.models import Todo, Profile
from todo.tests.factories import (
    UserFactory, TodoFactory, CommentFactory,
    GroupTaskFactory, GroupsFactory
        )

register(UserFactory)
register(TodoFactory)
register(CommentFactory)
register(GroupTaskFactory)
register(GroupsFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_authenticated(db, create_user, api_client):
    api_client.force_authenticate(user=create_user)
    yield api_client
    api_client.force_authenticate(user=None)

# @pytest.fixture
# def api_client_with_credentials_not_creator(db, user_factory, api_client):
#     api_client.force_login(user_factory)
#     yield api_client
#     api_client.logout()


@pytest.fixture
def task() -> Todo:
    return Todo.objects.create(title='test_title', description='test_description')


@pytest.fixture
def create_user(db, django_user_model, **kwargs):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return make_user
    # return Profile.objects.create(username='test_user', email='qwe@gmad.com', password='test_pass')
