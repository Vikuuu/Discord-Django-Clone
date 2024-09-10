from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Discord Clone API.",
        default_version="v1",
        description="API's for the Discord clone project.",
        contact=openapi.Contact(email="adivik672@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/friend/", include("friend.urls", namespace="friend")),
    path("api/chat/", include("chat.urls", namespace="chat")),
    path(
        "api/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-docs",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
