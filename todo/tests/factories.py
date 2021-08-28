from django.contrib.auth import get_user_model
import factory
from factory.django import DjangoModelFactory
from todo.models import Todo, Comments, GroupTask, Groups


User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = 'Axe'
    email = 'qwe@test.com'
    id = 1
    # username = factory.Sequence(lambda n: f"User{n}")
    # email = factory.Sequence(lambda n: f"user{n}p@test.com")


class TodoFactory(DjangoModelFactory):
    class Meta:
        model = Todo

    title = 'test_title'
    author = factory.SubFactory(UserFactory)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comments

    todo = factory.SubFactory(TodoFactory)
    author = factory.SubFactory(UserFactory)
    text = 'test_text'


class GroupTaskFactory(DjangoModelFactory):
    class Meta:
        model = GroupTask

    creator = factory.SubFactory(UserFactory)
    task_title = 'test_task_title'
    task_description = 'test_task_description'


class GroupsFactory(DjangoModelFactory):
    class Meta:
        model = Groups

    name = 'test_name'
    admin = factory.SubFactory(UserFactory)
    group_tasks = factory.SubFactory(UserFactory)
    users = factory.SubFactory(UserFactory)
