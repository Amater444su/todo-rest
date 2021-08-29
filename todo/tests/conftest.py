import ipdb
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from todo.models import Todo
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
def user():
    return UserFactory()


# @pytest.fixture
# def api_client():
#     return APIClient()


@pytest.fixture
def api_client_authenticated(db, user):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


# @pytest.fixture
# def task() -> Todo:
#     return Todo.objects.create(title='test_title', description='test_description')
