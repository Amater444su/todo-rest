import ipdb
from rest_framework import serializers
from .models import Todo, Profile, Comments

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



