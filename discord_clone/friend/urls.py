from django.urls import path
from .views import (
    SendFriendRequestView,
    AcceptFriendRequestView,
)

app_name = "friend"

urlpatterns = [
    path(
        "send/<str:username>/",
        SendFriendRequestView.as_view(),
        name="send",
    ),
    path(
        "accept/<str:username>/",
        AcceptFriendRequestView.as_view(),
        name="accept",
    ),
]
