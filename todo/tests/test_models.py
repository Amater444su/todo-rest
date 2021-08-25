import ipdb
import pytest


@pytest.mark.django_db
class TestModels:

    def test_todo_exist(self, task):
        assert task
