import ipdb
import pytest
from mixer.backend.django import mixer
from todo.models import Todo, Profile


@pytest.fixture
def task() -> Todo:
    return Todo.objects.create(title='test_title', description='test_description')


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return make_user
