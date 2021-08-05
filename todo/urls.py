from rest_framework import routers
from .views import *
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', TodoView.as_view(), name='todo'),
    path('todo-edit/<int:pk>', TodoDetailView.as_view(), name='todo-edit'),
    path('todo-edit/<int:todo_id>/comments/', CommentCreateView.as_view(), name='todo-comment'),
    path('todo-create/', TodoCreate.as_view(), name='todo-create'),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('group-create/', GroupsCreateView.as_view(), name='group_create'),
    path('group/', GroupsView.as_view(), name='group'),
    path('group/<int:pk>/', GroupsDetailView.as_view(), name='group_detail'),
    path('users-group/', GroupListDetailView.as_view(), name='users_group'),
    path('group/<int:group_id>/remove/<int:user_id>/', GroupsDeleteUsersView.as_view(), name='group_detail'),
    path('group/<int:group_id>/task/', GroupTaskView.as_view(), name='grouptast_create')


]

# router = routers.DefaultRouter()
# router.register('todo', TodoViewSet, 'todo')
# router.register('todo_edit/', TodoDetail, name='todoD')
# router.urls

