from rest_framework import serializers
from .models import Todo
# Сериалайзер что бы представлять модель в JSON формате, и для валидации данных.


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
