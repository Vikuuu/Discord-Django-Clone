from django.urls import path
from .views import SendFriendRequestView

app_name = "friend"

urlpatterns = [
    path("send/<str:username>/", SendFriendRequestView.as_view(), name="send"),
]
