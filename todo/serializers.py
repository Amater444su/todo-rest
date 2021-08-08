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
        fields = ['id', 'task_title', 'task_description', 'creator', 'worker', 'status', 'deadline']
        read_only_fields = ('status', 'deadline', )

    # def create(self, validated_data):
    #     pass


class GroupsSerializer(serializers.ModelSerializer):
    admin = serializers.SlugRelatedField(slug_field='username', read_only=True)
    group_tasks = GroupTaskSerializer(read_only=True, many=True)
    users = serializers.SlugRelatedField(slug_field='username', read_only=True, many=True)

    class Meta:
        model = Groups

        fields = ['id', 'name', 'admin', 'group_tasks', 'users']
