from rest_framework import routers
from .views import TodoViewSet, TodoDetail


router = routers.DefaultRouter()
router.register('todo', TodoViewSet, 'todo')
# router.register('todo_edit/', TodoDetail, name='todoD')


urlpatterns = router.urls
