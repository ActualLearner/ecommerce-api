from django.urls import path, include
from rest_framework import routers
from shop.views import (
    ProductViewSet,
    CategoryViewSet,
    CartViewSet,
    CartItemViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cart-items", CartItemViewSet, basename="cart-item")

urlpatterns = [
    path("", include(router.urls)),
]
