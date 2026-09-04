# E-Commerce API

A production-style E-Commerce REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **JWT authentication**.

The API provides user authentication, product management, cart functionality, and order checkout with automatic stock management.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Migrations](#database-migrations)
  - [Running the API](#running-the-api)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [API Reference](#api-reference)
  - [Products](#products)
  - [Cart](#cart)
  - [Orders](#orders)
  - [Health Check](#health-check)
- [Testing](#testing)
- [Docker](#docker)
- [Security](#security)
- [Current Limitations](#current-limitations)
- [License](#license)

---

## Features

- User registration and authentication
- JWT-based authentication
- Password hashing with Argon2
- Product CRUD operations
- Product search and filtering
- Price and stock filtering
- Pagination and sorting
- Category management through database relationships
- User cart management
- Order checkout with automatic stock deduction
- PostgreSQL database with SQLAlchemy ORM
- Alembic database migrations
- API testing with Pytest
- Docker and Docker Compose configuration

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2 |
| Migrations | Alembic |
| Validation | Pydantic |
| Auth | JWT / python-jose |
| Password Hashing | pwdlib + Argon2 |
| Testing | Pytest |
| Server | Uvicorn |
| Containerization | Docker |

## Project Structure

```text
ecommerce-api/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── category.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   └── orders.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   └── order_service.py
│   │
│   └── workers/
│       └── tasks.py
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── test_auth.py
│   ├── test_products.py
│   └── test_orders.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── pytest.ini
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL (running locally or accessible remotely)
- (Optional) Docker and Docker Compose

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/SAJLENDRAPANDEY/ecommerce-api.git
cd ecommerce-api
```

**2. Create and activate a virtual environment**

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_db
```

Ensure PostgreSQL is running and that the `ecommerce_db` database exists before proceeding.

### Database Migrations

Apply all migrations:

```powershell
alembic upgrade head
```

Check the current migration state:

```powershell
alembic current
```

The database schema includes the following tables:

- `users`
- `categories`
- `products`
- `orders`
- `order_items`
- `alembic_version`

### Running the API

Start the development server:

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Documentation

Interactive documentation is generated automatically by FastAPI:

| Interface | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

## Authentication

### Register

```http
POST /auth/register
```

**Request body**

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "test12345"
}
```

### Login

```http
POST /auth/login
```

**Request body**

```json
{
  "email": "test@example.com",
  "password": "test12345"
}
```

**Response**

```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "token_type": "bearer"
}
```

Include the token on subsequent requests to protected endpoints:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## API Reference

### Products

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/products/` | List products (search, filter, paginate, sort) | No |
| GET | `/products/{product_id}` | Retrieve a single product | No |
| POST | `/products/` | Create a product | Yes |
| PUT | `/products/{product_id}` | Update a product | Yes |
| DELETE | `/products/{product_id}` | Delete a product | Yes |

`GET /products/` supports the following query parameters:

- `search` — text search across product fields
- `min_price` / `max_price` — price range filtering
- `page` / `limit` — pagination
- `sort_by` — field to sort by
- `order` — `asc` or `desc`

Example:

```text
GET /products/?search=laptop&min_price=10000&max_price=100000&page=1&limit=10&sort_by=price&order=asc
```

### Cart

> The current cart implementation is user-specific and maintained in application memory (see [Current Limitations](#current-limitations)).

| Method | Endpoint | Description |
|---|---|---|
| POST | `/cart/add/{product_id}` | Add a product to the cart |
| GET | `/cart/` | View the current cart |
| DELETE | `/cart/{product_id}` | Remove a product from the cart |
| DELETE | `/cart/` | Clear the cart |

All cart endpoints require authentication.

### Orders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/orders/` | Checkout — creates an order from the current cart |
| GET | `/orders/` | List the authenticated user's orders |
| GET | `/orders/{order_id}` | Retrieve a single order |

Checkout performs the following steps:

1. Validates cart products
2. Checks product stock availability
3. Creates the order
4. Creates order items
5. Reduces product stock
6. Clears the cart

All order endpoints require authentication.

### Health Check

```http
GET /health
```

**Response**

```json
{
  "status": "Healthy"
}
```

## Testing

Run the full test suite:

```powershell
pytest -v
```

Current test coverage includes:

- User registration
- Health check
- Authentication protection
- Product listing
- Product not found
- Authenticated product creation
- Order authentication protection

Current result: **8 passed**

## Docker

The project ships with a `Dockerfile` and `docker-compose.yml`. The Compose configuration includes:

- The FastAPI application
- A PostgreSQL database
- A persistent PostgreSQL volume

Start the services:

```bash
docker compose up --build
```

Run migrations inside the running API container:

```bash
docker compose exec api alembic upgrade head
```

The API will be available at `http://localhost:8000`.

> Docker is configured in the project but requires Docker Desktop/Engine to be installed locally to run the containers.

## Security

- Passwords are stored as Argon2 hashes.
- JWT tokens protect authenticated endpoints.
- Passwords are never returned in API responses.
- Database credentials are configured through environment variables.

For production deployment, use a strong, unique secret key and secure database credentials.

## Current Limitations

- Cart data is currently stored in application memory rather than a database.
- Docker is configured but requires Docker Desktop/Engine to run locally.
- Redis/Celery are not yet implemented.

## License

This project is intended for learning, portfolio, and development purposes.
