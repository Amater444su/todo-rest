from rest_framework import routers
from .views import TodoViewSet, TodoDetail, TodoCreate
from django.urls import path, include


router = routers.DefaultRouter()
# router.register('todo', TodoViewSet, 'todo')
# router.register('todo_edit/', TodoDetail, name='todoD')


urlpatterns = [
    path('', TodoViewSet.as_view(), name='todo'),
    path('todo-edit/<int:pk>', TodoDetail.as_view(), name='todo-edit'),
    path('todo-create/', TodoCreate.as_view(), name='todo-create')

]
# router.urls

