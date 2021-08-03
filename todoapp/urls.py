from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/token/', obtain_auth_token, name='token'),

]
