from django import urls
from django.contrib.auth import get_user_model
import pytest


@pytest.mark.django_db
@pytest.mark.parametrize('param', [
    ('todo')
])
def test_render_views(client, param):
    # client (instance django test client) can simulate post and get requests
    temp_url = urls.reverse(param)
    response = client.get(temp_url)
    assert response.status_code == 200


def test_user_create_todo(client):
    pass