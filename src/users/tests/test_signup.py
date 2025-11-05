from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

User = get_user_model()


# By using a class, we only need one decorator for all tests within it.
@pytest.mark.django_db
class TestUserSignup:
    # Use the client as an instance variable, `self.client`
    # This ensures each test method runs in isolation, which is a best practice.
    def setup_method(self):
        self.client = APIClient()

    def test_signup_success(self):
        """
        GIVEN: Valid user registration data is provided.
        WHEN: A POST request is made to the user creation endpoint.
        THEN: A new user should be created with is_active=False, and a 201 status is returned.
        """
        user_data = {
            "email": "test_success@example.com",
            "password": "someSecurePassword123",
            "re_password": "someSecurePassword123",
            "first_name": "Test",
            "last_name": "User",
        }
        response = self.client.post("/api/v1/auth/users/", user_data, format="json")

        assert response.status_code == 201
        assert response.data["email"] == user_data["email"]
        assert response.data["first_name"] == user_data["first_name"]

        # Verify the user was actually created in the database and is inactive
        user = User.objects.get(email=user_data["email"])
        assert user.is_active is False
        assert user.last_name == "User"

    def test_signup_fails_if_email_already_exists(self):
        """
        GIVEN: An email address that is already registered.
        WHEN: A new registration request is made with that email.
        THEN: The request should fail with a 400 status.
        """
        # First, create a user to ensure the email exists
        existing_user = User.objects.create_user(
            email="existing@example.com", password="password123"
        )

        user_data = {
            "email": "existing@example.com",
            "password": "someOtherPassword",
            "re_password": "someOtherPassword",
        }
        response = self.client.post("/api/v1/auth/users/", user_data, format="json")

        assert response.status_code == 400
        # Make the assertion more specific
        assert "user with this email already exists." in str(response.data["email"])

    def test_signup_fails_if_passwords_do_not_match(self):
        """
        GIVEN: Registration data where password and re_password differ.
        WHEN: A registration request is made.
        THEN: The request should fail with a 400 status.
        """
        user_data = {
            "email": "mismatch@example.com",
            "password": "passwordA",
            "re_password": "passwordB",
        }
        response = self.client.post("/api/v1/auth/users/", user_data, format="json")
        # TODO: REMOVE DEUBG LINES
        print("==========RESPONSE==========")
        print(response.data)

        assert response.status_code == 400
        assert "password" in str(
            response.data
        )  # Djoser uses a non_field_error for this

    def test_signup_fails_if_email_is_missing(self):
        """
        GIVEN: Registration data without an email field.
        WHEN: A registration request is made.
        THEN: The request should fail with a 400 status.
        """
        user_data = {
            "password": "someSecurePassword123",
            "re_password": "someSecurePassword123",
        }
        response = self.client.post("/api/v1/auth/users/", user_data, format="json")

        assert response.status_code == 400
        assert "This field is required." in str(response.data["email"])

    def test_signup_succeeds_with_unrecognized_fields(self):
        """
        GIVEN: A payload containing extra, unrecognized fields.
        WHEN: A registration request is made.
        THEN: The user should still be created successfully, ignoring the extra fields.
        """
        user_data = {
            "age": 99,  # This field is not in our UserCreateSerializer
            "favorite_color": "blue",
            "email": "extrafields@example.com",
            "password": "someSecurePassword123",
            "re_password": "someSecurePassword123",
        }
        response = self.client.post("/api/v1/auth/users/", user_data, format="json")

        assert response.status_code == 201
        assert "age" not in response.data
        assert User.objects.filter(email=user_data["email"]).exists()
