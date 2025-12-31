# FastAPI Product Management API

A lightweight RESTful API for managing product inventory and seller accounts, built with FastAPI and SQLAlchemy. This project provides a simple yet robust backend solution for product CRUD (Create, Read, Update, Delete) operations and seller registration with SQLite database persistence.

## Overview

This API enables developers to build product management systems with essential features for creating, retrieving, updating, and deleting product records, as well as secure seller account registration. It's ideal for e-commerce applications, inventory management systems, or as a learning resource for FastAPI development.

### Key Features

- **Full CRUD Operations**: Complete product lifecycle management
- **Seller Registration**: Secure user account creation with password hashing
- **Password Security**: Bcrypt-based password hashing using passlib
- **RESTful API Design**: Clean, intuitive endpoint structure
- **SQLite Database**: Lightweight, file-based data persistence
- **SQLAlchemy ORM**: Type-safe database interactions
- **Pydantic Validation**: Automatic request/response validation
- **Response Model Filtering**: Control which fields are exposed in API responses
- **HTTP Status Codes**: Proper status code handling (201 Created for POST endpoints)
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc
- **Dependency Injection**: Efficient database session management

## Architecture

The project follows a modular architecture with clear separation of concerns:

```
fastapi_project/
├── Product/
│   ├── main.py          # API endpoints and route handlers
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic schemas for validation
│   └── database.py      # Database configuration and session management
├── main.py              # Application entry point (optional)
├── requirements.txt     # Python dependencies
└── product.db          # SQLite database file (auto-generated)
```

### Components

- **Models** ([Product/models.py](Product/models.py)): Defines the database schema using SQLAlchemy ORM (Product and Seller tables)
- **Schemas** ([Product/schemas.py](Product/schemas.py)): Pydantic models for request/response validation (includes DisplaySeller for response filtering)
- **Database** ([Product/database.py](Product/database.py)): Database engine configuration and session factory
- **API Routes** ([Product/main.py](Product/main.py)): FastAPI endpoints for product operations and seller registration
- **Security** ([Product/main.py](Product/main.py:16)): Password hashing context using passlib with bcrypt

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

No additional environment variables are required. The application uses SQLite with a local database file (`product.db`) that will be created automatically on first run.

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

Used for GET endpoints to control response data. This schema **excludes the price field** for privacy/security.

```json
{
  "name": "string",
  "description": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Product name |
| `description` | string | Product description |

**Note:** The `price` field is intentionally hidden in GET responses using the `DisplayProduct` response model.

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
    "description": "High-performance laptop with 16GB RAM"
  },
  {
    "name": "Mouse",
    "description": "Wireless ergonomic mouse"
  }
]
```

**Note:** This endpoint uses the `DisplayProduct` response model, which filters out the `price` field for privacy/security purposes.

##### Get Single Product

**Request:**
```bash
curl -X GET "http://localhost:8000/product/1"
```

**Response:**
```json
{
  "name": "Laptop",
  "description": "High-performance laptop with 16GB RAM"
}
```

**Note:** This endpoint uses the `DisplayProduct` response model, which filters out the `price` field for privacy/security purposes.

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

# Create a product
new_product = {
    "name": "Keyboard",
    "description": "Mechanical gaming keyboard",
    "price": 8999
}
response = requests.post(f"{BASE_URL}/product", json=new_product)
print(response.json())
print(f"Status Code: {response.status_code}")  # 201 Created

# Get all products (returns DisplayProduct - no price field)
response = requests.get(f"{BASE_URL}/products")
products = response.json()
print(f"Total products: {len(products)}")
# Output: [{"name": "Keyboard", "description": "Mechanical gaming keyboard"}, ...]

# Get specific product (returns DisplayProduct - no price field)
product_id = 1
response = requests.get(f"{BASE_URL}/product/{product_id}")
print(response.json())
# Output: {"name": "Keyboard", "description": "Mechanical gaming keyboard"}

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

**Database Configuration** ([Product/database.py](Product/database.py:6))
- Uses SQLite for lightweight, file-based storage
- Connection string: `sqlite:///./product.db`
- Configured with `check_same_thread=False` for FastAPI compatibility

**Models** ([Product/models.py](Product/models.py))
- `Product` table with auto-incrementing ID, name, description, and price fields
- `Seller` table with auto-incrementing ID, username, email, and password fields
- Indexed primary keys for efficient queries

**Schemas** ([Product/schemas.py](Product/schemas.py))
- `Product`: Full schema for input validation (create/update operations)
- `DisplayProduct`: Filtered schema for GET responses (excludes price field)
- `Seller`: Full schema for seller registration input
- `DisplaySeller`: Filtered schema for seller responses (excludes password field)
- Uses Pydantic v2 with `from_attributes = True` for SQLAlchemy compatibility

**Security** ([Product/main.py](Product/main.py:16))
- `pwd_context`: Password hashing context using passlib with bcrypt
- Passwords are automatically hashed before database storage
- Uses bcrypt version 4.1.2 for secure password hashing

**Dependency Injection** ([Product/main.py](Product/main.py:18-23))
- `get_db()` function provides database sessions
- Automatic session cleanup with try/finally pattern

**Response Models** ([Product/main.py](Product/main.py:46-56))
- GET endpoints use `response_model=DisplayProduct` to filter sensitive data
- Uses `List[DisplayProduct]` for list endpoints
- Provides data privacy by hiding price information in public endpoints

**HTTP Status Codes** ([Product/main.py](Product/main.py:58))
- POST `/product` endpoint returns 201 Created status code
- Proper REST API status code implementation

### Adding New Features

To extend the API with additional functionality:

1. **Add a new field to an existing model:**
   - Update the model in [Product/models.py](Product/models.py)
   - Update the corresponding schema in [Product/schemas.py](Product/schemas.py)
   - Delete `product.db` to recreate the database with new schema

2. **Add a new database table:**
   - Create a new model class in [Product/models.py](Product/models.py)
   - Create corresponding Pydantic schemas in [Product/schemas.py](Product/schemas.py)
   - Consider creating a Display schema to filter sensitive fields
   - Add endpoints in [Product/main.py](Product/main.py)

3. **Add a new endpoint:**
   - Define the route in [Product/main.py](Product/main.py)
   - Use dependency injection for database access
   - Follow existing patterns for consistency
   - Use appropriate HTTP status codes

4. **Implement password hashing for new user models:**
   - Import `CryptContext` from passlib
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
- [ ] Use DisplaySeller response model to hide password hash from responses
- [ ] Add seller login/authentication with JWT tokens
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

---

**Happy coding!** If you find this project useful, please consider giving it a star on GitHub.
