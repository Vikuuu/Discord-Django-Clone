"""
URL mapping for the user API.
"""

from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("create/", views.UserRegistrationView.as_view(), name="create"),
]
