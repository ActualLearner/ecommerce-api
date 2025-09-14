# E-commerce API: Lightweight Software Requirements Specification (SRS)

## Introduction
This document outlines the software requirements for an MVP e-commerce API. The API will facilitate basic e-commerce functionalities such as user authentication, product discovery, shopping cart management, and order processing. All endpoints will be versioned under `/api/v1/`.

## Features
- Signup & login
- Product Discovery
- Shopping Cart & Checkout
- Product Management

### Main Actors
Admins & Users

## User Stories

### Authentication
- As a user, I want to sign up so that I can start shopping.
- As a returning user, I want to log in so that I can access my account.

### Product Discovery
- As a user, I want to view all products so that I can choose what to buy.
- As a user, I want to view detailed information about a single product so that I can make an informed purchase decision.
- As a user, I want to search for a specific product by name.
- As a user, I want to filter products by categories.

### Shopping Cart & Checkout
- As a user, I want to add products to my cart so that I can purchase them later.
- As a user, I want to view my cart so that I can see what I've added.
- As a user, I want to update the quantity of an item in my cart so that I can adjust my order.
- As a user, I want to remove an item from my cart if I change my mind.
- As a user, I want to place an order from my cart so that I can complete my purchase.

### Product Management
- As an admin, I want to add a new product so that users can buy it.
- As an admin, I want to modify the price or stock of an existing product so that the catalog is always up-to-date.
- As an admin, I want to delete a product that is no longer for sale.

## Functional Requirements

### Authentication
- The system shall provide a `POST /api/v1/auth/register/` endpoint that accepts user information. When the information is provided, the system shall create a new user.
- The system shall provide a `POST /api/v1/auth/login/` endpoint that accepts user information. When the information is provided, the system shall verify that user and return a JWT token on success.

### Product Discovery
- The system shall provide a `GET /api/v1/products/` endpoint. When the endpoint is requested, the system shall return a paginated response of the products.
- The system shall allow the product list endpoint to accept a `search` query parameter. When a product name is provided, the system shall return products containing that name.
- The system shall allow the product list endpoint to accept a `category` query parameter. When a category ID is provided, the system shall return only the products belonging to that category.
- The system shall provide a `GET /api/v1/products/{id}/` endpoint. When requested, the system shall return the full details of a single product.

### Shopping Cart & Checkout
- The system shall provide a `GET /api/v1/cart/` endpoint for an authenticated user to retrieve their current cart items.
- The system shall provide a `POST /api/v1/cart/add/` endpoint that accepts a product ID and quantity to add an item to the user's cart.
- The system shall provide a `PUT /api/v1/cart/item/{item_id}/` endpoint to update the quantity of a specific item in the user's cart.
- The system shall provide a `DELETE /api/v1/cart/item/{item_id}/` endpoint to remove a specific item from the user's cart.
- The system shall provide a `POST /api/v1/orders/` endpoint that processes the current user's cart into an order. When this endpoint is requested, the system shall create an order, clear the user's cart, and return the order details.

### Product Management (Admin Access Required)
- The system shall allow a `POST` request to `/api/v1/products/`. When valid product information is provided, the system shall create a new product.
- The system shall allow `PUT` or `PATCH` requests to `/api/v1/products/{id}/`. When a product ID is provided with valid product information, the system shall update the product's information.
- The system shall allow a `DELETE` request to `/api/v1/products/{id}/`. When requested, the endpoint shall delete the product with the provided ID.