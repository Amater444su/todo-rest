from rest_framework import routers
from .views import TodoView, TodoDetailView, TodoCreate, CommentCreateView
from django.urls import path, include


router = routers.DefaultRouter()
# router.register('todo', TodoViewSet, 'todo')
# router.register('todo_edit/', TodoDetail, name='todoD')


urlpatterns = [
    path('', TodoView.as_view(), name='todo'),
    path('todo-edit/<int:pk>', TodoDetailView.as_view(), name='todo-edit'),
    path('todo-edit/<int:todo_id>/comments/', CommentCreateView.as_view(), name='todo-comment'),
    path('todo-create/', TodoCreate.as_view(), name='todo-create')

]
# router.urls

