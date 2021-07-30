from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


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
