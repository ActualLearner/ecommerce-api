# Project Nexus - E-Commerce REST API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)![Django REST Framework](https://img.shields.io/badge/Django%20REST-A30000?style=for-the-badge&logo=django&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

A robust, production-ready REST API for a modern e-commerce platform. This project serves as the final portfolio piece for the ALX Backend Engineering bootcamp, showcasing a mastery of backend principles from secure authentication and database design to deployment and CI/CD.

The API provides a complete backend solution for managing products, categories, user accounts, shopping carts, and order processing, with a focus on scalability, maintainability, and security.

**Live Demo:**
- **Connected Frontend:** [**https://alxpd.aymenab.com/**](https://alxpd.aymenab.com/)
- **Backend API Docs (Swagger UI):** [**https://ecommerce-api-glia.onrender.com/api/v1/docs/**](https://ecommerce-api-glia.onrender.com/api/v1/docs/)
## Table of Contents

- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Post-MVP & Future Scope](#post-mvp--future-scope)
- [License](#license)
- [Contact](#contact)

## Key Features

- **Secure JWT Authentication**: Stateless authentication using JSON Web Tokens with refresh token rotation and blacklisting for enhanced security. Users can log in with their email.
- **Full E-Commerce Workflow**: Complete shopping cart and order management. Users can add/update items in their cart, and the checkout process creates a permanent order, validates stock, and decrements inventory in an atomic transaction.
- **Product & Category Management**: Full CRUD operations for products and categories, restricted to admin users.
- **Advanced Product Discovery**: Robust filtering by category and powerful search across product names and descriptions.
- **Optimized Performance**: Implemented database indexing and efficient serializers to ensure fast queries and lightweight responses.
- **Global Pagination**: All list endpoints are paginated to ensure fast and predictable responses.
- **Automated API Documentation**: Integrated Swagger UI and ReDoc for comprehensive, interactive API documentation, automatically generated from the code.

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: `djangorestframework-simplejwt`
- **API Documentation**: `drf-spectacular` (OpenAPI 3.0)
- **Containerization**: Docker, Docker Compose
- **Environment Management**: `django-environ`
- **Production Server**: Gunicorn, Whitenoise

## API Documentation

The API is fully documented using OpenAPI 3.0 and is live on Render.

- **Live Swagger Docs**: [**https://ecommerce-api-glia.onrender.com/api/v1/docs/**](https://ecommerce-api-glia.onrender.com/api/v1/docs/)

For local development, the interactive UI can be accessed at:

- **Local Swagger Docs**: `http://localhost:8000/api/v1/docs/`
- **Local ReDoc**: `http://localhost:8000/api/v1/redoc/`

## Project Structure

The project follows a professional, scalable nested `src` layout.

```
.
├── src/
│   ├── config/           # Project-level settings, URLs, etc.
│   ├── shop/             # App for products, cart, and orders
│   ├── users/            # App for user management & authentication
│   └── manage.py         # Django's command-line utility
├── .env.example          # Example environment variables
├── compose.yaml          # Docker Compose configuration for production
├── compose.dev.yaml      # Docker Compose overrides for development
├── Dockerfile            # Production Docker configuration
├── Dockerfile.dev        # Development Docker configuration
└── README.md
```

## Getting Started

Follow these instructions to get a local copy up and running for development.

### Prerequisites

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/products/docker-desktop/) & Docker Compose

### Setup & Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/ActualLearner/ecommerce-api.git
    cd ecommerce-api
    ```

2.  **Create the environment file:**
    Create a `.env` file for your local environment variables. For development, ensure `DEBUG=True`.
    ```sh
    cp .env.example .env
    ```
    *Update the `.env` file with your local settings. The default values are configured to work with the provided Docker Compose setup.*

## Running the Application

The entire application stack (Django API and PostgreSQL database) is managed by Docker Compose.

1.  **Build and run the development containers:**
    This command uses `compose.dev.yaml` to enable live-reloading.
    ```sh
    docker-compose -f compose.yaml -f compose.dev.yaml up --build -d
    ```
    *(Alternatively, add `COMPOSE_FILE=compose.yaml:compose.dev.yaml` to your `.env` file and simply run `docker-compose up --build -d`)*

2.  **Apply database migrations:**
    ```sh
    docker-compose -f compose.yaml -f compose.dev.yaml exec web python manage.py makemigrations shop
    docker-compose -f compose.yaml -f compose.dev.yaml exec web python manage.py migrate
    ```

3.  **Create a superuser (Admin):**
    ```sh
    docker-compose -f compose.yaml -f compose.dev.yaml exec web python manage.py createsuperuser
    ```

The API will be accessible at `http://localhost:8000/`.

## Post-MVP & Future Scope

This project has a solid foundation. Future enhancements planned include:

- [x] Shopping Cart & Checkout Logic
- [x] Full Order Management Flow
- [ ] Payment Gateway Integration (e.g., Stripe)
- [ ] User Email Verification on Registration
- [ ] Automated Testing Suite (Unit & Integration Tests)
- [ ] CI/CD Pipeline with GitHub Actions

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Abdellah Shafi - [@ActualLearner](https://twitter.com/ActualLearner) - abdellahshafi7@google.com

Project Link: [https://github.com/ActualLearner/ecommerce-api](https://github.com/ActualLearner/ecommerce-api)
