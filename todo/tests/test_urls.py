from django.urls import reverse, resolve

from todo.views import *


class TestUrls:

    def test_todo_url(self):
        path = reverse('todo')
        # ipdb.set_trace()
        assert resolve(path).view_name == 'todo'
