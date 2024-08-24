"""
Serializers for the Models.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User Model Serializer."""

    password = serializers.CharField(
        write_only=True,
        max_length=255,
        min_length=8,
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "display_name", "dob", "password"]

    def validate_dob(self, value):
        """Validates the date of birth."""
        today = timezone.now().date()

        if value > today:
            raise serializers.ValidationError(
                "Date of birth cannot be in the future."
            )

        age = (
            today.year
            - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )
        if age < 18:
            raise serializers.ValidationError(
                "You must be at least 18 years old to register."
            )

        return value

    def validate(self, attrs):
        """Validates the field values entered."""
        if (
            get_user_model()
            .objects.filter(
                username=attrs["username"],
            )
            .exists()
        ):
            raise serializers.ValidationError(
                "Account with this username already exists!"
            )
        if get_user_model().objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                "Account with this email address already exists!"
            )

        return attrs

    def create(self, validated_data):
        """Create and return user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """Serializer for loging in the user."""

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(min_length=8, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """Serializer to return the User information."""

    class Meta:
        model = get_user_model()
        fields = ["username", "display_name", "email"]
