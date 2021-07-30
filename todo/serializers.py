from rest_framework import serializers
from .models import Todo, Profile, Comments

# Сериалайзер что бы представлять модель в JSON формате, и для валидации данных.


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['text']


class TodoSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'categories', 'author', 'comment']


class TodoCreateSerializer(serializers.ModelSerializer):
    # todos = serializers.PrimaryKeyRelatedField(many=False, queryset=Todo.objects.all())

    class Meta:
        model = Todo
        fields = ['title', 'description', 'categories']


class TodoDetailSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(write_only=True)

    class Meta:
        model = Todo
        fields = ['title', 'description', 'categories', 'comment']



