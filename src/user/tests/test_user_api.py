"""
Tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    """Helper function to create and return new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the public feature of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": "test@example.com",
            "username": "test",
            "display_name": "Test User",
            "dob": "2006-08-23",
            "password": "testpass123",
        }
        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", result.data)
        self.assertEqual(user.display_name, payload["display_name"])
        dob_from_user = user.dob.strftime("%Y-%m-%d")
        self.assertEqual(dob_from_user, payload["dob"])

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": "test@example.com",
            "username": "test",
            "display_name": "Test User",
            "dob": "2006-08-23",
            "password": "testpass123",
        }
        create_user(**payload)
        payload["username"] = "newtest"
        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_username_existes_error(self):
        """Test error returned if user with username exists."""
        payload = {
            "email": "test@example.com",
            "username": "test",
            "display_name": "Test User",
            "dob": "2006-08-23",
            "password": "testpass123",
        }
        create_user(**payload)
        payload["email"] = "test1@example.com"
        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test error is returned if password is less than 8 chars."""
        payload = {
            "email": "test@example.com",
            "username": "test",
            "display_name": "Test User",
            "dob": "2006-08-23",
            "password": "testpas",
        }
        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )
        self.assertFalse(user_exists)

    def test_dob_less_than_18_error(self):
        """Test error is returned if dob is less than 18 years"""
        payload = {
            "email": "test@example.com",
            "username": "test",
            "display_name": "Test User",
            "dob": "2007-08-23",
            "password": "testpas",
        }
        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )
        self.assertFalse(user_exists)

    def test_dob_future_error(self):
        """Test error is returned if dob is of future."""
        payload = {
            "email": "test@example.com",
            "username": "test",
            "display_name": "Test User",
            "dob": "2025-08-23",
            "password": "testpas",
        }
        result = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )
        self.assertFalse(user_exists)
