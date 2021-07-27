from rest_framework import routers
from .views import TodoViewSet, UserViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register('todo', TodoViewSet, 'todo')
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)



urlpatterns = router.urls
