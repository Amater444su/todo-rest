from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class GroupTaskStatuses(models.TextChoices):
    NOT_DONE = 'Not done'
    IN_PROCESS = 'In process'
    DONE = 'Done'
    OUT_OF_DATE = 'Out of date'


class TodoCategories(models.TextChoices):
    HOMEWORK = 'Домашнее задание'
    HOUSEWORK = 'Дела по дому'


class Profile(AbstractUser):
    address = models.CharField(max_length=40, blank=True, null=True, verbose_name='address')
    phone_number = models.CharField(max_length=12, null=True, blank=True, verbose_name='Phone number', validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,16}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ])


class Todo(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Todo_posts')
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=300, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    categories = models.CharField(choices=TodoCategories.choices, max_length=40, blank=True, null=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='todo_comment', verbose_name='Заметка')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_comment',
                               verbose_name='Пользователь')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    text = models.TextField(verbose_name='Текст коментария')


class GroupTask(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='creator')
    worker = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='worker', null=True, blank=True)
    task_title = models.CharField(max_length=100)
    task_description = models.TextField()
    task_start_time = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=GroupTaskStatuses.choices, default=GroupTaskStatuses.NOT_DONE)


class Groups(models.Model):
    name = models.CharField(max_length=50, default='My group')
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='admin')
    group_tasks = models.ManyToManyField(GroupTask, related_name='group_tasks', null=True, blank=True)
    users = models.ManyToManyField(Profile, related_name='users', null=True, blank=True)
