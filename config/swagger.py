from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config.settings import DEFAULT_URL


TodoREST_schema_view = get_schema_view(
   openapi.Info(
      title="TodoREST API",
      default_version='v1',
      description="TodoREST documentation",
   ),
   url=DEFAULT_URL,
   public=True,
   permission_classes=(permissions.IsAdminUser,),
   patterns=[
       path("todo/", include("todo.urls", namespace="todo")),
   ],
)
