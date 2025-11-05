from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from shop.models import Category, Product
import pytest

User = get_user_model()


@pytest.mark.django_db
class TestShopPermissions(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.regular_user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="password"
        )
        self.category = Category.objects.create(
            name="Test Category", description="A test category"
        )
        self.product_data = {
            "name": "Test Product",
            "description": "A test product",
            "price": "99.99",
            "stock": 10,
            "category": self.category.id,
        }

    def test_product_listing_is_public(self):
        response = self.client.get("/api/v1/shop/products/")
        self.assertEqual(response.status_code, 200)

    def test_create_product_fails_for_unauthenticated_user(self):
        response = self.client.post(
            "/api/v1/shop/products/", self.product_data, format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_create_product_fails_for_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post("/api/v1/shop/products/", self.product_data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_create_product_succeeds_for_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/v1/shop/products/", self.product_data, format="json")
        self.assertEqual(response.status_code, 201)
        # We can also assert that the product was actually created
        self.assertTrue(Product.objects.filter(name=self.product_data["name"]).exists())

    def test_product_modification_is_restricted_to_admins(self):
        product = Product.objects.create(
            name="Another Product", price=10, stock=5, category=self.category
        )

        self.client.force_authenticate(user=self.regular_user)
        response = self.client.patch(
            f"/api/v1/shop/products/{product.id}/", {"price": "20.00"}, format="json"
        )
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            f"/api/v1/shop/products/{product.id}/", {"price": "20.00"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
