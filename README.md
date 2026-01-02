# FastAPI Product Management API

A lightweight RESTful API for managing product inventory and seller accounts, built with FastAPI and SQLAlchemy. This project provides a simple yet robust backend solution for product CRUD (Create, Read, Update, Delete) operations, seller registration, and JWT-based authentication with SQLite database persistence.

## Overview

This API enables developers to build product management systems with essential features for creating, retrieving, updating, and deleting product records, as well as secure seller account registration and JWT-based authentication. It's ideal for e-commerce applications, inventory management systems, or as a learning resource for FastAPI development with authentication.

### Key Features

- **Full CRUD Operations**: Complete product lifecycle management
- **JWT Authentication**: Secure token-based authentication with OAuth2 password bearer flow
- **Seller Registration**: Secure user account creation with password hashing
- **Seller Login**: Authentication endpoint with JWT token generation
- **Product-Seller Relationships**: Products linked to sellers via foreign keys with bidirectional relationships
- **Nested Response Models**: Product responses include seller information
- **Password Security**: Bcrypt-based password hashing using passlib
- **Token-Based Security**: JWT tokens with configurable expiration (20 minutes default)
- **Modular Router Architecture**: Organized code with separate routers for each resource type
- **RESTful API Design**: Clean, intuitive endpoint structure
- **SQLite Database**: Lightweight, file-based data persistence
- **SQLAlchemy ORM**: Type-safe database interactions with relationships
- **Pydantic Validation**: Automatic request/response validation
- **Response Model Filtering**: Control which fields are exposed in API responses
- **HTTP Status Codes**: Proper status code handling (201 Created for POST endpoints)
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc with organized tags
- **Dependency Injection**: Efficient database session management

## Architecture

The project follows a modular architecture with clear separation of concerns and router-based organization:

```
fastapi_project/
├── Product/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── product.py   # Product-related endpoints
│   │   ├── seller.py    # Seller-related endpoints
│   │   └── login.py     # Authentication endpoints (JWT login)
│   ├── main.py          # Application setup and router registration
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic schemas for validation
│   └── database.py      # Database configuration and session management
├── main.py              # Application entry point (optional)
├── requirements.txt     # Python dependencies
└── product.db          # SQLite database file (auto-generated)
```

### Components

- **Models** ([Product/models.py](Product/models.py)): Defines the database schema using SQLAlchemy ORM (Product and Seller tables with relationships)
- **Schemas** ([Product/schemas.py](Product/schemas.py)): Pydantic models for request/response validation with nested models (DisplayProduct includes DisplaySeller, Login, Token, TokenData)
- **Database** ([Product/database.py](Product/database.py)): Database engine configuration and session factory
- **Main Application** ([Product/main.py](Product/main.py)): FastAPI app setup, router registration, and metadata configuration
- **Product Router** ([Product/routers/product.py](Product/routers/product.py)): Product CRUD endpoints (GET, POST, PUT, DELETE)
- **Seller Router** ([Product/routers/seller.py](Product/routers/seller.py)): Seller registration endpoint with password hashing
- **Login Router** ([Product/routers/login.py](Product/routers/login.py)): Authentication endpoint with JWT token generation and password verification

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Application                       │
│                         (Product/main.py)                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  App Metadata: Title, Description, Contact, Docs Config    │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        │ includes routers
        ┌───────────────┼───────────────┬───────────────┐
        │               │               │               │
        ▼               ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Product    │ │    Seller    │ │    Login     │ │  Future      │
│   Router     │ │    Router    │ │    Router    │ │  Routers...  │
│              │ │              │ │              │ │              │
│ product.py   │ │  seller.py   │ │  login.py    │ │  (expandable)│
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────────────┘
       │                │                │
       │ uses           │ uses           │ uses
       │                │                │
       ├────────────────┴────────────────┴─────────────┬─────────────┐
       │                               │             │
       ▼                               ▼             ▼
┌──────────────┐              ┌──────────────┐ ┌──────────────┐
│   Schemas    │              │   Models     │ │   Database   │
│  (Pydantic)  │              │ (SQLAlchemy) │ │   Session    │
│              │              │              │ │              │
│ schemas.py   │              │  models.py   │ │ database.py  │
│              │              │              │ │              │
│ - Product    │              │ - Product    │ │ - Engine     │
│ - Display    │              │   Table      │ │ - SessionMkr │
│   Product    │              │ - Seller     │ │ - get_db()   │
│ - Seller     │              │   Table      │ │   dependency │
│ - Display    │              │ - Relations  │ │              │
│   Seller     │              │              │ │              │
└──────────────┘              └──────┬───────┘ └──────────────┘
                                     │
                                     │ persists to
                                     ▼
                              ┌──────────────┐
                              │   SQLite     │
                              │   Database   │
                              │              │
                              │ product.db   │
                              └──────────────┘

Request Flow:
─────────────
HTTP Request → FastAPI App → Router → Validate with Schema →
→ Query Database via Model → Return Response (filtered by Display Schema)
```

### Why Router-Based Architecture?

The project has been refactored to use FastAPI's APIRouter pattern, which provides several advantages:

**Benefits:**
- **Separation of Concerns**: Each router handles a specific resource type (products, sellers), making code easier to understand and maintain
- **Scalability**: Easy to add new resource types by creating new router files without cluttering the main application
- **Team Collaboration**: Different team members can work on different routers without conflicts
- **Testing**: Individual routers can be tested in isolation
- **Code Organization**: Related endpoints are grouped together with clear file boundaries
- **Reusability**: Routers can be reused across different FastAPI applications
- **Clean Main File**: The main.py file focuses on app configuration and router registration, not business logic

**How It Works:**
1. Each router file (e.g., [product.py](Product/routers/product.py)) creates an `APIRouter()` instance with configuration:
   - `prefix`: URL prefix for all routes in the router (e.g., `"/product"`)
   - `tags`: OpenAPI tags for grouping endpoints in documentation
2. Endpoints are decorated with `@router.get()`, `@router.post()`, etc. instead of `@app.get()`
3. Route paths in decorators are simplified (e.g., `@router.get('/{id}')` instead of `@router.get('/product/{id}')`) because the prefix is applied automatically
4. Routers are registered in [main.py](Product/main.py:18-19) using `app.include_router()`
5. All endpoints from registered routers become part of the main FastAPI application

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd fastapi_project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup

The application uses SQLite with a local database file (`product.db`) that will be created automatically on first run.

**JWT Authentication Configuration:**

The application uses environment variables for JWT configuration. A `.env` file is included with a secure secret key.

**For Development:**
- The `.env` file is already configured with a secure random key
- No additional setup needed - just run the application

**For Production:**
1. Generate a new secure secret key: `openssl rand -hex 32`
2. Set environment variables in your hosting platform:
   ```bash
   JWT_SECRET_KEY=your-production-secret-key
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=20
   ```
3. Never commit the production secret key to version control

**Security Note:** The `.env` file is already in `.gitignore` to prevent accidentally committing secrets to version control.

### Running the Application

Start the development server with:

```bash
uvicorn Product.main:app --reload
```

The API will be available at:
- **Base URL**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## API Reference

### Endpoints

#### Product Endpoints

| Method | Endpoint | Description | Request Body | Status Code |
|--------|----------|-------------|--------------|-------------|
| `GET` | `/products` | Retrieve all products | None | 200 OK |
| `GET` | `/product/{id}` | Retrieve a single product by ID | None | 200 OK |
| `POST` | `/product` | Create a new product | Product object | 201 Created |
| `PUT` | `/product/{id}` | Update an existing product by ID | Product object | 200 OK |
| `DELETE` | `/product/{id}` | Delete a product by ID | None | 200 OK |

#### Seller Endpoints

| Method | Endpoint | Description | Request Body | Status Code |
|--------|----------|-------------|--------------|-------------|
| `POST` | `/seller` | Create a new seller account | Seller object | 200 OK |

#### Authentication Endpoints

| Method | Endpoint | Description | Request Body | Status Code |
|--------|----------|-------------|--------------|-------------|
| `POST` | `/login` | Authenticate seller and receive JWT token | Login credentials | 200 OK |

### Data Models

The API uses Pydantic schemas for request/response validation:

#### Product Schemas

##### Product Schema (Input)

Used for creating and updating products.

```json
{
  "name": "string",
  "description": "string",
  "price": integer
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Product name |
| `description` | string | Yes | Product description |
| `price` | integer | Yes | Product price (in cents or smallest currency unit) |

##### DisplayProduct Schema (Output)

Used for GET endpoints to control response data. This schema **excludes the price field** for privacy/security and **includes nested seller information**.

```json
{
  "name": "string",
  "description": "string",
  "seller": {
    "username": "string",
    "email": "string"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Product name |
| `description` | string | Product description |
| `seller` | DisplaySeller | Seller information (username and email) |

**Note:** The `price` field is intentionally hidden in GET responses using the `DisplayProduct` response model. Seller information is included through a nested `DisplaySeller` object.

#### Seller Schemas

##### Seller Schema (Input)

Used for creating seller accounts.

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Seller's username |
| `email` | string | Yes | Seller's email address |
| `password` | string | Yes | Seller's password (will be hashed with bcrypt) |

##### DisplaySeller Schema (Output)

Used for seller registration responses. This schema **excludes the password field** for security.

```json
{
  "username": "string",
  "email": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `username` | string | Seller's username |
| `email` | string | Seller's email address |

**Note:** The `password` field is never returned in responses. Passwords are hashed using bcrypt before storage.

#### Authentication Schemas

##### Login Schema (Input)

Used for authenticating sellers.

```json
{
  "username": "string",
  "password": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Seller's username |
| `password` | string | Yes | Seller's password (plaintext for authentication) |

##### Token Schema (Output)

Returned after successful authentication.

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | JWT access token (valid for 20 minutes) |
| `token_type` | string | Token type (always "bearer") |

##### TokenData Schema

Internal schema for JWT token payload.

| Field | Type | Description |
|-------|------|-------------|
| `username` | string (optional) | Username extracted from JWT token |

**Note:** JWT tokens are signed using HS256 algorithm and expire after 20 minutes by default.

### Usage Examples

#### Product Operations

##### Create a Product

**Request:**
```bash
curl -X POST "http://localhost:8000/product" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop with 16GB RAM",
    "price": 129999
  }'
```

**Response:** (Status: 201 Created)
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High-performance laptop with 16GB RAM",
  "price": 129999
}
```

##### Get All Products

**Request:**
```bash
curl -X GET "http://localhost:8000/products"
```

**Response:**
```json
[
  {
    "name": "Laptop",
    "description": "High-performance laptop with 16GB RAM",
    "seller": {
      "username": "john_seller",
      "email": "john@example.com"
    }
  },
  {
    "name": "Mouse",
    "description": "Wireless ergonomic mouse",
    "seller": {
      "username": "john_seller",
      "email": "john@example.com"
    }
  }
]
```

**Note:** This endpoint uses the `DisplayProduct` response model, which filters out the `price` field for privacy/security purposes and includes the seller information for each product.

##### Get Single Product

**Request:**
```bash
curl -X GET "http://localhost:8000/product/1"
```

**Response:**
```json
{
  "name": "Laptop",
  "description": "High-performance laptop with 16GB RAM",
  "seller": {
    "username": "john_seller",
    "email": "john@example.com"
  }
}
```

**Note:** This endpoint uses the `DisplayProduct` response model, which filters out the `price` field for privacy/security purposes and includes the seller information.

##### Update a Product

**Request:**
```bash
curl -X PUT "http://localhost:8000/product/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "description": "High-performance gaming laptop with RTX 4080",
    "price": 199999
  }'
```

**Response:**
```json
{
  "Product: 1 is successfully updated"
}
```

##### Delete a Product

**Request:**
```bash
curl -X DELETE "http://localhost:8000/product/1"
```

**Response:**
```json
{
  "message": "Product deleted successfully",
  "id": 1
}
```

#### Seller Operations

##### Create a Seller Account

**Request:**
```bash
curl -X POST "http://localhost:8000/seller" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_seller",
    "email": "john@example.com",
    "password": "SecurePassword123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "username": "john_seller",
  "email": "john@example.com",
  "password": "$2b$12$hashed_password_string_here"
}
```

**Note:** The password is automatically hashed using bcrypt before storage. In production, you may want to use the `DisplaySeller` response model to hide the hashed password from the response.

#### Authentication Operations

##### Login to Get JWT Token

**Request:**
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_seller",
    "password": "SecurePassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX3NlbGxlciIsImV4cCI6MTcwOTQ5MzYwMH0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "token_type": "bearer"
}
```

**Authentication Flow:**
1. Seller provides username and password
2. System verifies username exists in database
3. System verifies password using bcrypt hash comparison
4. If valid, system generates JWT token with:
   - Subject (`sub`): username
   - Expiration (`exp`): current time + 20 minutes
5. Returns access token and token type

**Error Responses:**
- Invalid username: `404 Not Found` - "Invalid user"
- Invalid password: `404 Not Found` - "Invalid password"

**Note:** The JWT token expires after 20 minutes. Store the token securely and include it in the `Authorization` header for protected endpoints.

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a seller account
new_seller = {
    "username": "alice_seller",
    "email": "alice@example.com",
    "password": "MySecurePassword456"
}
response = requests.post(f"{BASE_URL}/seller", json=new_seller)
print(response.json())
# Output: {"id": 1, "username": "alice_seller", "email": "alice@example.com", "password": "$2b$12$..."}

# Login to get JWT token
login_credentials = {
    "username": "alice_seller",
    "password": "MySecurePassword456"
}
response = requests.post(f"{BASE_URL}/login", json=login_credentials)
token_data = response.json()
access_token = token_data["access_token"]
print(f"Access Token: {access_token}")
# Output: Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Use the token in subsequent requests (for future protected endpoints)
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Create a product
new_product = {
    "name": "Keyboard",
    "description": "Mechanical gaming keyboard",
    "price": 8999
}
response = requests.post(f"{BASE_URL}/product", json=new_product)
print(response.json())
print(f"Status Code: {response.status_code}")  # 201 Created

# Get all products (returns DisplayProduct with seller info, no price field)
response = requests.get(f"{BASE_URL}/products")
products = response.json()
print(f"Total products: {len(products)}")
# Output: [{"name": "Keyboard", "description": "Mechanical gaming keyboard", "seller": {"username": "alice_seller", "email": "alice@example.com"}}, ...]

# Get specific product (returns DisplayProduct with seller info, no price field)
product_id = 1
response = requests.get(f"{BASE_URL}/product/{product_id}")
print(response.json())
# Output: {"name": "Keyboard", "description": "Mechanical gaming keyboard", "seller": {"username": "alice_seller", "email": "alice@example.com"}}

# Update product
updated_product = {
    "name": "Wireless Keyboard",
    "description": "Mechanical gaming keyboard with RGB",
    "price": 12999
}
response = requests.put(f"{BASE_URL}/product/{product_id}", json=updated_product)
print(response.json())

# Delete product
response = requests.delete(f"{BASE_URL}/product/{product_id}")
print(response.json())
```

## Development

### Project Structure Details

**Database Configuration** ([Product/database.py](Product/database.py))
- Uses SQLite for lightweight, file-based storage
- Connection string: `sqlite:///./product.db`
- Configured with `check_same_thread=False` for FastAPI compatibility
- Provides `get_db()` dependency for session management

**Models** ([Product/models.py](Product/models.py))
- `Product` table with auto-incrementing ID, name, description, price, and seller_id fields
- `Seller` table with auto-incrementing ID, username, email, and password fields
- Foreign key relationship: Product.seller_id → Seller.id
- Bidirectional relationships: Product.seller and Seller.products
- Indexed primary keys for efficient queries

**Schemas** ([Product/schemas.py](Product/schemas.py))
- `Product`: Full schema for input validation (create/update operations)
- `DisplayProduct`: Filtered schema for GET responses (excludes price field, includes nested DisplaySeller)
- `Seller`: Full schema for seller registration input
- `DisplaySeller`: Filtered schema for seller responses (excludes password field)
- Nested models: DisplayProduct contains DisplaySeller to show product ownership
- Uses Pydantic v2 with `from_attributes = True` for SQLAlchemy compatibility

**Router Pattern** ([Product/routers/](Product/routers/))
- Modular organization using FastAPI's APIRouter
- Separate routers for different resource types (products, sellers)
- Each router is independently testable and maintainable
- Routers are registered in [Product/main.py](Product/main.py:18-19) using `app.include_router()`

**Product Router** ([Product/routers/product.py](Product/routers/product.py))
- Configured with `prefix="/product"` and `tags=['Product']` for clean URL structure and documentation grouping
- All product CRUD operations (GET, POST, PUT, DELETE)
- Simplified route paths (e.g., `/{id}` instead of `/product/{id}`) due to prefix configuration
- Uses `response_model=DisplayProduct` for GET endpoints to filter sensitive data
- Returns 201 Created status code for POST operations
- Proper error handling with HTTPException for 404 cases

**Seller Router** ([Product/routers/seller.py](Product/routers/seller.py))
- Configured with `tags=['Seller']` for documentation grouping
- Seller registration endpoint
- Password hashing using passlib with bcrypt
- `pwd_context` configured with bcrypt scheme
- Passwords are automatically hashed before database storage

**Login Router** ([Product/routers/login.py](Product/routers/login.py))
- Configured with `tags=['Login']` for documentation grouping
- JWT-based authentication endpoint
- Password verification using passlib with bcrypt
- Token generation using python-jose library
- Token configuration:
  - Algorithm: HS256 (configurable via environment variable)
  - Expiration: 20 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
  - Secret key: Loaded from environment variables for security
- Authentication flow: username lookup → password verification → JWT token generation
- Returns token in OAuth2 bearer token format
- Proper error handling with 404 status codes for invalid credentials

**Main Application** ([Product/main.py](Product/main.py))
- FastAPI app initialization with metadata (title, description, contact info)
- Router registration for modular endpoint organization (product, seller, login)
- Database table creation on startup
- Customizable API documentation URLs

### Adding New Features

To extend the API with additional functionality using the router pattern:

1. **Add a new field to an existing model:**
   - Update the model in [Product/models.py](Product/models.py)
   - Update the corresponding schema in [Product/schemas.py](Product/schemas.py)
   - Update the relevant router endpoint if needed
   - Delete `product.db` to recreate the database with new schema

2. **Add a new database table with its own router:**
   - Create a new model class in [Product/models.py](Product/models.py)
   - Create corresponding Pydantic schemas in [Product/schemas.py](Product/schemas.py)
   - Consider creating a Display schema to filter sensitive fields
   - Add relationships if needed (foreign keys and bidirectional relationships)
   - **Create a new router file** in [Product/routers/](Product/routers/) (e.g., `category.py`)
   - Register the new router in [Product/main.py](Product/main.py) using `app.include_router()`

3. **Add a new endpoint to an existing resource:**
   - Add the route to the appropriate router file ([product.py](Product/routers/product.py) or [seller.py](Product/routers/seller.py))
   - Use dependency injection for database access with `db: Session = Depends(get_db)`
   - Follow existing patterns for consistency
   - Use appropriate HTTP status codes (201 for POST, 404 for not found)
   - No need to add `tags` to individual routes since they're configured in the router initialization

4. **Create a new router module:**
   ```python
   # Product/routers/new_resource.py
   from fastapi import APIRouter, Depends
   from sqlalchemy.orm import Session
   from ..database import get_db
   from .. import schemas, models

   router = APIRouter(
       tags=['Resource'],
       prefix="/resource"
   )

   @router.get('/')
   def get_resources(db: Session = Depends(get_db)):
       # Your implementation
       pass
   ```
   Then register in [Product/main.py](Product/main.py):
   ```python
   from .routers import product, seller, new_resource
   app.include_router(new_resource.router)
   ```

   **Best Practice:** Configure `tags` and `prefix` in the APIRouter initialization rather than in individual route decorators for cleaner, more maintainable code.

5. **Implement password hashing for new user models:**
   - Import `CryptContext` from passlib in your router
   - Create `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")`
   - Use `pwd_context.hash(password)` before storing passwords
   - Never return plaintext or hashed passwords in responses

### Common Customizations

**Change Database to PostgreSQL:**

Update [Product/database.py](Product/database.py:6):
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

**Enable CORS for Frontend Integration:**

Add to [Product/main.py](Product/main.py):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Secure JWT Configuration with Environment Variables:**

Update [Product/routers/login.py](Product/routers/login.py) to use environment variables:
```python
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key-for-development")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20"))
```

Then set environment variables before running:
```bash
export JWT_SECRET_KEY=$(openssl rand -hex 32)
export ACCESS_TOKEN_EXPIRE_MINUTES=30
uvicorn Product.main:app --reload
```

## Testing

### Manual Testing

Use the interactive Swagger UI at http://localhost:8000/docs to test all endpoints with a visual interface.

### Automated Testing

Create a `tests/` directory and add test files:

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from Product.main import app

client = TestClient(app)

def test_create_product():
    response = client.post("/product", json={
        "name": "Test Product",
        "description": "Test Description",
        "price": 1000
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

Run tests with:
```bash
pip install pytest
pytest tests/
```

## Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
   - Follow existing code style and conventions
   - Add tests for new features
   - Update documentation as needed
4. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of your changes"
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**

### Code Style Guidelines

- Follow PEP 8 for Python code formatting
- Use type hints where applicable
- Write descriptive commit messages
- Keep functions focused and single-purpose
- Add docstrings for complex functions

### Reporting Issues

Found a bug or have a feature request? Please open an issue on GitHub with:
- Clear description of the problem or suggestion
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Your environment details (OS, Python version)

## License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Roadmap

Future enhancements under consideration:

- [x] Add PUT endpoint for updating products
- [x] Implement seller registration with password hashing
- [x] Add HTTP status code 201 for POST endpoints
- [x] Add seller login/authentication with JWT tokens
- [x] Move SECRET_KEY to environment variables for security
- [ ] Use DisplaySeller response model to hide password hash from responses
- [ ] Implement protected endpoints using JWT authentication
- [ ] Implement pagination for product listings
- [ ] Add search and filtering capabilities
- [ ] Include product categories/tags
- [ ] Add authorization and role-based access control
- [ ] Implement rate limiting
- [ ] Add comprehensive error handling
- [ ] Add email validation for seller registration
- [ ] Create Docker containerization
- [ ] Set up CI/CD pipeline
- [ ] Add request/response logging
- [ ] Implement password strength validation

## Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check existing documentation at http://localhost:8000/docs
- Review the code examples in this README

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Uvicorn](https://www.uvicorn.org/) - ASGI server
- [Passlib](https://passlib.readthedocs.io/) - Password hashing library
- [Bcrypt](https://github.com/pyca/bcrypt/) - Secure password hashing algorithm
- [Python-JOSE](https://python-jose.readthedocs.io/) - JWT token creation and validation

---

**Happy coding!** If you find this project useful, please consider giving it a star on GitHub.
