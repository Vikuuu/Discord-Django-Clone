"""
Serializers for the Models.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from user.models import UserProfile


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


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for User account model. To be referenced in Profile serializer."""

    class Meta:
        model = get_user_model()
        fields = ["username", "display_name", "email", "dob"]


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer to return the User Profile Info."""

    user = UserProfileSerializer()

    class Meta:
        model = UserProfile
        fields = ["photo", "user"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        # getting the user profile key from the serializer.
        profile_representation = representation.get("user", {})
        representation["owner"] = True

        if instance.user != request.user:
            profile_representation.pop("email", None)
            profile_representation.pop("dob", None)
            representation["owner"] = False

        representation["user"] = profile_representation

        return representation

    def update(self, instance, validated_data):
        if "user" in validated_data:
            nested_serializer = self.fields["user"]
            nested_instance = instance.user

            nested_data = validated_data.pop("user", None)
            nested_serializer.update(nested_instance, nested_data)

        return super(ProfileSerializer, self).update(instance, validated_data)
