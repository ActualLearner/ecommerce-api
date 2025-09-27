# Project Nexus - E-Commerce REST API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)![Django REST Framework](https://img.shields.io/badge/Django%20REST-A30000?style=for-the-badge&logo=django&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

A robust, production-ready REST API for a modern e-commerce platform. This project serves as the final portfolio piece for the ALX Backend Engineering bootcamp, showcasing a mastery of backend principles, including secure authentication, database design, API documentation, and performance optimization.

The API provides a complete backend solution for managing products, categories, and user accounts, with a clear separation of concerns and a focus on scalability and maintainability.

## Table of Contents

- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
  - [Using Docker (Recommended)](#using-docker-recommended)
  - [Local Python Environment](#local-python-environment)
- [Post-MVP & Future Scope](#post-mvp--future-scope)
- [License](#license)
- [Contact](#contact)

## Key Features

- **Secure JWT Authentication**: Stateless authentication using JSON Web Tokens. Users can register and log in with either their **username or email**. Features secure token rotation for enhanced security.
- **Product & Category Management**: Full CRUD (Create, Read, Update, Delete) operations for products and categories, restricted to admin users for security.
- **Advanced Product Discovery**: Robust filtering capabilities allow users to find products by category slug. Includes powerful search functionality across product names and descriptions.
- **Optimized Performance**: Implemented database indexing on key fields to ensure fast query performance. Employs a "list vs. detail" serializer pattern to serve lightweight data for lists and detailed data for single objects.
- **Global Pagination**: All list endpoints are paginated to ensure fast and predictable responses, preventing server overload.
- **Automated API Documentation**: Integrated Swagger UI and ReDoc for comprehensive, interactive API documentation, automatically generated from the code.

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: `djangorestframework-simplejwt`
- **API Documentation**: `drf-spectacular` (OpenAPI 3.0)
- **Containerization**: Docker, Docker Compose
- **Environment Management**: `django-environ`

## API Documentation

The API is fully documented using OpenAPI 3.0. Once the application is running, the interactive Swagger UI can be accessed at:

- **Swagger Docs**: `http://localhost:8000/api/v1/docs/`
- **ReDoc**: `http://localhost:8000/api/v1/redoc/`

The raw schema file is also available for generating clients or importing into tools like Postman:

- **Schema**: `http://localhost:8000/api/v1/schema/`

## Project Structure

The project follows a professional, scalable nested `src` layout with Django's management utility inside the source directory.

```
.
├── docs/                 # Requirements and design documents
├── src/
│   ├── config/           # Project-level settings, URLs, etc.
│   ├── shop/             # App for products, categories, orders
│   ├── users/            # App for user management & authentication
│   └── manage.py         # Django's command-line utility
├── .env                  # Environment variables (Git-ignored)
├── compose.yaml          # Docker Compose configuration
├── Dockerfile            # Docker configuration for the Django app
├── README.md
└── requirements.txt      # Python package dependencies
```

## Getting Started

Follow these instructions to get a local copy of the project up and running for development and testing purposes.

### Prerequisites

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/products/docker-desktop/) & [Docker Compose](https://docs.docker.com/compose/install/) (for containerized setup)
- [Python 3.10+](https://www.python.org/) & `pip` (for local setup)
- A running PostgreSQL instance (for local setup)

### Setup & Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-github-username/ecommerce-api.git
    cd ecommerce-api
    ```

2.  **Create the environment file:**
    Create a `.env` file in the project root by copying the example file. This file contains sensitive information like your `SECRET_KEY` and database credentials.
    ```sh
    cp .env.example .env
    ```
    **Important:** Update the `DATABASE_URL` in the `.env` file if you are running PostgreSQL locally and not with Docker.

## Running the Application

You can run the application using either Docker or a local Python environment.

### Using Docker (Recommended)

The entire application stack (Django API and PostgreSQL database) is managed by Docker Compose.

1.  **Build and run the containers:**
    From the project root, run the following command.
    ```sh
    docker-compose up --build -d
    ```

2.  **Apply database migrations:**
    ```sh
    docker-compose exec web python src/manage.py migrate
    ```

3.  **Create a superuser (Admin):**
    ```sh
    docker-compose exec web python src/manage.py createsuperuser
    ```

The API will be accessible at `http://localhost:8000/`.

### Local Python Environment

1.  **Set up a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3.  **Apply database migrations:**
    ```sh
    python src/manage.py migrate
    ```

4.  **Create a superuser (Admin):**
    ```sh
    python src/manage.py createsuperuser
    ```

5.  **Run the development server:**
    ```sh
    python src/manage.py runserver
    ```

The API will be accessible at `http://localhost:8000/`.

## Post-MVP & Future Scope

This MVP lays a solid foundation. Future enhancements planned for this project include:
- [ ] Shopping Cart & Checkout Logic
- [ ] Full Order Management Flow
- [ ] Payment Gateway Integration (e.g., Stripe)
- [ ] User Email Verification on Registration
- [ ] Automated Testing Suite

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Abdellah Shafi - [@ActualLearner](https://twitter.com/ActualLearner) - abdellahshafi7@google.com

Project Link: [https://github.com/ActualLearner/ecommerce-api](https://github.com/ActualLearner/ecommerce-api)
