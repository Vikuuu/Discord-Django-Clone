"""
Views for Registering and Authenticating the Users.
"""

from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
)
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .utils import JwtTokens
from core.backends import JwtAuthentication
from .models import UserToken
from django.utils import timezone
from datetime import timedelta


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

            access_token = JwtTokens.create_access_token(user.id)
            refresh_token = JwtTokens.create_refresh_token(user.id)

            UserToken.objects.create(
                user=user,
                token=refresh_token,
                expired_at=timezone.now() + timedelta(days=7),
            )

            response = Response()
            response.set_cookie(
                key="refresh_token", value=refresh_token, httponly=True
            )
            response.data = {"token": access_token}
            response.status_code = status.HTTP_200_OK

            return response

        except AuthenticationFailed as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        except UserToken.DoesNotExist:
            return Response(
                {"error": "Error Saving token, Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return Response(
                {"error": "Unexpected error occured " + str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserView(generics.GenericAPIView):
    """Returns the Authenticated User."""

    serializer_class = UserSerializer
    authentication_classes = [JwtAuthentication]

    def get(self, request):
        return Response(self.get_serializer(request.user).data)


class RefreshTokenView(views.APIView):
    """
    Returns the Access token for the corresponding Refresh
    token present in the Cookies.
    """

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        id = JwtTokens.decode_refresh_token(refresh_token)

        if not UserToken.objects.filter(
            user=id, token=refresh_token, expired_at__gt=timezone.now()
        ).exists():
            raise AuthenticationFailed("Unauthenticated")

        access_token = JwtTokens.create_access_token(id)

        return Response({"token": access_token})


class UserLogoutView(views.APIView):
    """
    Removes the Current refresh token in the Cookies
    and from the Token Database.
    """

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        UserToken.objects.filter(token=refresh_token).delete()

        response = Response()
        response.delete_cookie(key="refresh_token")
        response.data = {"message": "success"}

        return response
