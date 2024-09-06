"""
URL mapping for the user API.
"""

from django.urls import path
from user.views import (
    UserRegistrationView,
    UserLoginView,
    UserView,
    RefreshTokenView,
    UserLogoutView,
    UserProfileView,
)

app_name = "user"

urlpatterns = [
    path("create/", UserRegistrationView.as_view(), name="create"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("me/", UserView.as_view(), name="me"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/<str:username>/", UserProfileView.as_view(), name="profile"),
]
