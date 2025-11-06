from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.mark.django_db
class TestAuthenticationFlow(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "password": "someSecurePassword123",
            "re_password": "someSecurePassword123",
            "username": "Test",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_registration_activation_and_login_workflow(self):
        # 1. Register User
        response = self.client.post(
            "/api/v1/auth/users/", self.user_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

        # 2. Verify User is Inactive
        user = User.objects.get(email=self.user_data["email"])
        self.assertFalse(user.is_active)

        # 3. Attempt Login (should fail)
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(
            "/api/v1/auth/jwt/create/", login_data, format="json"
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("No active account found", str(response.data))

        # 4. Activate User
        # The console email backend stores sent emails in `mail.outbox`
        self.assertEqual(len(mail.outbox), 1)
        activation_email = mail.outbox[0]
        # Extract uid and token from the email body (this is a bit complex but robust)
        email_body = activation_email.body
        uid_token_part = email_body.split("activate/")[1]
        # split only on the first slash
        uid, token_and_rest = uid_token_part.split("/", 1)
        # take only the first “word”, which is the token
        token = token_and_rest.split()[0]

        activation_data = {"uid": uid, "token": token}
        # TODO:REMOVE DEBUG LINES
        response = self.client.post(
            "/api/v1/auth/users/activation/", activation_data, format="json"
        )
        print("========RESPONSE=========")
        print(activation_data)
        print(response)
        print(response.data)
        self.assertEqual(response.status_code, 204)

        # 5. Verify User is Active
        user.refresh_from_db()
        self.assertTrue(user.is_active)

        # 6. Attempt Login (should succeed)
        response = self.client.post(
            "/api/v1/auth/jwt/create/", login_data, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_registration_fails_with_existing_email(self):
        # Create a user first
        User.objects.create_user(email=self.user_data["email"], password="somepassword")

        response = self.client.post(
            "/api/v1/auth/users/", self.user_data, format="json"
        )
        self.assertEqual(response.status_code, 400)
