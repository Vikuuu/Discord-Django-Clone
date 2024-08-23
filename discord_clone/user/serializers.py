"""
Serializers for the Models.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User Model Serializer."""

    password = serializers.CharField(
        write_only=True,
        max_length=255,
        min_length=8,
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password"]

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
