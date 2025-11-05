from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from shop.models import Category, Product, Cart, Order, Status
import pytest

User = get_user_model()


@pytest.mark.django_db
class TestFullPurchaseWorkflow(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="customer@example.com", password="password"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name="Electronics1", description="Gadgets"
        )
        self.product = Product.objects.create(
            name="Laptop", price="1200.00", stock=10, category=self.category
        )

    def test_complete_purchase_flow(self):
        # 1. Add item to cart
        add_to_cart_data = {"product_id": self.product.id, "quantity": 2}
        response = self.client.post(
            "/api/v1/shop/cart-items/", add_to_cart_data, format="json"
        )
        self.assertEqual(response.status_code, 201)

        # 2. Verify Cart
        response = self.client.get(f"/api/v1/shop/cart/{self.user.cart.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["cart_items"][0]["quantity"], 2)
        self.assertEqual(float(response.data["total_price"]), 2400.00)

        # 3. Create Order from cart
        response = self.client.post("/api/v1/shop/orders/", format="json")
        self.assertEqual(response.status_code, 201)

        # TODO: REMOVE DEBUG LINES
        print(response.data)
        order_id = response.data["id"]
        order = Order.objects.get(id=order_id)

        # 4. Verify Order state
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, Status.pending)
        self.assertEqual(order.order_items.count(), 1)
        self.assertEqual(float(order.total_price), 2400.00)

        # 5. Verify Stock Reduction
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)

        # 6. Verify Cart is Empty
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.cart_items.count(), 0)

    def test_order_creation_fails_when_stock_is_insufficient(self):
        add_to_cart_data = {
            "product_id": self.product.id,
            "quantity": 11,
        }  # Stock is 10
        response = self.client.post(
            "/api/v1/shop/cart-items/", add_to_cart_data, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Not enough stock", str(response.data))
