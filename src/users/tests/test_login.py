from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import pytest

User = get_user_model()


@pytest.mark.django_db
class TestLogin(TestCase):
    def setUp(self):
        """This method runs before each test in this class."""
        self.client = APIClient()
        self.credentials = {
            "email": "active_user@example.com",
            "password": "strongPassword123",
        }

        # Create a user who is already activated for login tests
        self.active_user = User.objects.create_user(
            email=self.credentials["email"],
            password=self.credentials["password"],
            is_active=True,
        )

    def test_login_success_for_active_user(self):
        response = self.client.post(
            "/api/v1/auth/jwt/create/", self.credentials, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_fails_with_wrong_password(self):
        invalid_credentials = {
            "email": self.credentials["email"],
            "password": "wrongPassword",
        }
        response = self.client.post(
            "/api/v1/auth/jwt/create/", invalid_credentials, format="json"
        )

        self.assertEqual(response.status_code, 401)
        # Djoser/SimpleJWT returns a standard error message for failed auth attempts
        self.assertIn(
            "No active account found with the given credentials", str(response.data)
        )

    def test_login_fails_for_inactive_user(self):
        inactive_user_credentials = {
            "email": "inactive_user@example.com",
            "password": "password123",
        }
        # Djoser's registration creates users as inactive by default
        User.objects.create_user(**inactive_user_credentials, is_active=False)

        response = self.client.post(
            "/api/v1/auth/jwt/create/", inactive_user_credentials, format="json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn(
            "No active account found with the given credentials", str(response.data)
        )

    def test_login_fails_for_nonexistent_user(self):
        nonexistent_credentials = {
            "email": "ghost@example.com",
            "password": "password123",
        }
        response = self.client.post(
            "/api/v1/auth/jwt/create/", nonexistent_credentials, format="json"
        )

        self.assertEqual(response.status_code, 401)
