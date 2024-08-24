"""
Views for Registering and Authenticating the Users.
"""

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
)
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserRegistrationView(generics.GenericAPIView):
    """Create a new user in system."""

    queryset = get_user_model().objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User created successfully.",
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(generics.GenericAPIView):
    """Login the User with the credentials."""

    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        try:
            user = authenticate(request, username=username, password=password)
            if user is None:
                raise AuthenticationFailed("Invalid Credentials.")
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
