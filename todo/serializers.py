import ipdb
from rest_framework import serializers
from .models import Todo, Comments, GroupTask, Groups

# Сериалайзер что бы представлять модель в JSON формате, и для валидации данных.


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['id', 'text']


class TodoSerializer(serializers.ModelSerializer):
    todo_comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'categories', 'author', 'todo_comment']


class TodoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['title', 'description', 'categories']


class TodoDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['title', 'description', 'categories']


class GroupTaskSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', read_only=True)
    worker = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = GroupTask
        fields = ['task_title', 'task_description', 'creator', 'worker', 'status']
        read_only_fields = ('status',)


class GroupsSerializer(serializers.ModelSerializer):
    admin = serializers.SlugRelatedField(slug_field='username', read_only=True)
    group_tasks = GroupTaskSerializer(read_only=True, many=True)
    users = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)

    class Meta:
        model = Groups

        fields = ['name', 'admin', 'group_tasks', 'users', 'task_amount']
        read_only_fields = ('task_amount', )
