"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test models."""

    def test_create_user_succesful(self):
        """Test creating a user with email and username successful."""
        email = "test@example.com"
        username = "test"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_and_usernae_normalized(self):
        """Test email and username is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@EXAMPLE.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        sample_usernames = [
            ["Testusername1", "testusername1"],
            ["TestUsername2", "testusername2"],
            ["TESTUSERNAME3", "testusername3"],
            ["testusernamE4", "testusername4"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                username=email.split("@")[0],
                password="testpass123",
            )
            self.assertEqual(user.email, expected)

        for username, expected in sample_usernames:
            user = get_user_model().objects.create_user(
                email=f"{username}@example.com",
                username=username,
                password="testpass123",
            )
            self.assertEqual(user.username, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a new user without email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="",
                username="test",
                password="test123",
            )

    def test_new_user_without_username_raises_error(self):
        """
        Test that creating a new user without username raises a ValurError.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email="test@example.com",
                username="",
                password="testpass123",
            )

    def test_create_superuser(self):
        """Test creating superuser."""
        user = get_user_model().objects.create_superuser(
            email="test@example.com",
            username="test",
            password="testpass123",
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
