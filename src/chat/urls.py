from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.private_chat_list, name="private_chat_list"),
    path(
        "start/<uuid:user_id>/",
        views.private_chat_start,
        name="private_chat_start",
    ),
    path("<uuid:pk>/", views.private_chat_detail, name="private_chat_detail"),
]
