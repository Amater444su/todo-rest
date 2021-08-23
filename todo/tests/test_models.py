# from django.db.models import Count
# from todo.models import *
# import pytest
#
#
# @pytest.mark.django_db
# class TestModels:
#
#     def test_todo_exist(self):
#         todo = Todo.objects.annotate(todo_count=Count('title'))
#         assert todo['todo_count'] > 0
