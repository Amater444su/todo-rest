from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Task-Manager API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('swagger/', schema_view),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/token/', obtain_auth_token, name='token'),

]
