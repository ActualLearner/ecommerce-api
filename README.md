# Project Nexus - E-Commerce REST API v2.0.0

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)![Django REST Framework](https://img.shields.io/badge/Django%20REST-A30000?style=for-the-badge&logo=django&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

A robust, production-ready REST API for a modern e-commerce platform. This project serves as the final portfolio piece for the ALX Backend Engineering bootcamp, showcasing a mastery of backend principles from secure authentication and database design to automated testing, deployment, and CI/CD.

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
- [Running Tests](#running-tests)
- [License](#license)
- [Contact](#contact)

## Key Features

- **Secure JWT Authentication**: Stateless authentication using `Djoser` and `simplejwt` with refresh token rotation.
- **Email Verification**: New users are created as inactive and must verify their email via an activation link, preventing spam and ensuring user validity.
- **Payment Gateway Integration**: Full payment workflow integrated with the Chapa payment gateway, including payment initialization and a secure webhook for transaction confirmation.
- **Full E-Commerce Workflow**: Complete shopping cart and order management. Users can add/update items in their cart, and the checkout process creates a permanent order, validates stock, and decrements inventory in an atomic, race-condition-safe transaction.
- **Robust Permissions**: Granular, role-based access control. Product and category management is restricted to admin users, while cart and order endpoints are protected for authenticated users.
- **Optimized Performance**: Implemented database indexing, `select_related`/`prefetch_related` for query optimization, and efficient serializers.
- **Automated Testing Suite**: Comprehensive integration test suite built with `pytest` and `pytest-django`, covering critical user journeys from registration to a paid order.
- **Continuous Integration (CI) Pipeline**: Automated CI pipeline using **GitHub Actions** to build, test, and validate every push and pull request, ensuring code quality and stability.
- **Automated API Documentation**: Integrated Swagger UI and ReDoc for comprehensive, interactive API documentation, automatically generated from the code using `drf-spectacular`.

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: `Djoser`, `djangorestframework-simplejwt`
- **Payment Integration**: Chapa API
- **API Documentation**: `drf-spectacular` (OpenAPI 3.0)
- **Testing**: `pytest`, `pytest-django`
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, Docker Compose
- **Production Server**: Gunicorn, Whitenoise

## API Documentation

The API is fully documented using OpenAPI 3.0 and is live on Render.

- **Live Swagger Docs**: [**https://ecommerce-api-glia.onrender.com/api/v1/docs/**](https://ecommerce-api-glia.onrender.com/api/v1/docs/)

For local development, the interactive UI can be accessed at:

- **Local Swagger Docs**: `http://localhost:8000/api/v1/docs/`
- **Local ReDoc**: `http://localhost:8000/api/v1/redoc/`

## Project Structure

The project follows a professional flat layout, separating Python source code from project management files, and relies on a `.dockerignore` file for clean container builds.

```
.
├── .github/
│   └── workflows/
│       └── ci.yaml         # GitHub Actions CI pipeline configuration
│
├── src/
│   ├── pytest.ini          # Pytest configuration
│   ├── config/             # Project-level settings, URLs, etc.
│   ├── shop/               # App for products, cart, and orders
│   ├── users/              # App for user management & authentication
│   ├── payment/            # App for payment integration
│   └── manage.py           # Django's command-line utility
│
├── .dockerignore           # Specifies files to exclude from Docker image
├── .env.example            # Example environment variables
├── compose.dev.yaml        # Docker Compose overrides for development
├── compose.yaml            # Main Docker Compose configuration
├── Dockerfile              # Production-ready, multi-stage Docker configuration
├── entrypoint.sh           # Production startup script
├── render.yaml             # Infrastructure-as-Code for Render deployment
├── requirements.txt        # Python project dependencies
└── README.md
```

## Getting Started

Follow these instructions to get a local copy up and running for development.

### Prerequisites

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/products/docker-desktop/) & Docker Compose

### Setup & Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/ActualLearner/ecommerce-api.git
    cd ecommerce-api
    ```

2. **Create the environment file:**
    Create a `.env` file for your local environment variables. For development, ensure `DEBUG=True` and `EMAIL_BACKEND` is set to the console backend.

    ```sh
    cp .env.example .env
    ```

    *Update the `.env` file with your local settings. The default values are configured to work with the provided Docker Compose setup.*

## Running the Application

The entire application stack (Django API and PostgreSQL database) is managed by Docker Compose.

1. **Build and run the development containers:**
    This command uses `compose.dev.yaml` to enable live-reloading.

    ```sh
    docker compose -f compose.yaml -f compose.dev.yaml up --build -d
    ```

2. **Apply database migrations:**

    ```sh
    docker compose exec web python manage.py migrate
    ```

3. **Create a superuser (Admin):**

    ```sh
    dockercompose exec web python manage.py createsuperuser
    ```

The API will be accessible at `http://localhost:8000/`.

## Running Tests

The project has a comprehensive test suite. The test environment is fully containerized.

1. **Run the entire test suite:**

    ```sh
    docker compose exec web pytest
    ```

2. **Run tests for a specific app:**

    ```sh
    docker compose exec web pytest src/shop/
    ```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Abdellah Shafi - [@ActualLearner](https://twitter.com/ActualLearner) - <abdellahshafi7@gmail.com>

Project Link: [https://github.com/ActualLearner/ecommerce-api](https://github.com/ActualLearner/ecommerce-api)
