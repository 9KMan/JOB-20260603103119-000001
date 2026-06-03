# Inventory & Operations System

A full-stack inventory management system built with FastAPI, PostgreSQL, and a responsive frontend.

## Features

- **Authentication**: JWT-based user authentication with bcrypt password hashing
- **Inventory Management**: Full CRUD operations for inventory items with SKU, RFID support
- **Operations Tracking**: Track inventory movements (ADD, REMOVE, ADJUST, AUDIT)
- **Responsive UI**: Modern, mobile-friendly interface
- **RESTful API**: Versioned API endpoints (/api/v1/...)

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Vanilla HTML/CSS/JS (can be replaced with any framework)
- **Auth**: JWT (HS256), bcrypt
- **Migrations**: Alembic
- **Container**: Docker & Docker Compose

## Quick Start

### Using Docker Compose

```bash
docker-compose up --build
```

The API will be available at http://localhost:8000
API docs at http://localhost:8000/api/docs

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/inventory_db"
export SECRET_KEY="your-secret-key"

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Inventory
- `GET /api/v1/inventory/` - List all items
- `POST /api/v1/inventory/` - Create new item
- `GET /api/v1/inventory/{id}` - Get item by ID
- `PUT /api/v1/inventory/{id}` - Update item
- `DELETE /api/v1/inventory/{id}` - Soft delete item

### Operations
- `GET /api/v1/operations/` - List operations
- `POST /api/v1/operations/` - Create operation

## Data Model

- **Users**: id, email, password_hash, full_name, is_active, timestamps
- **InventoryItems**: id, sku, name, description, quantity, location, rfid_tag, user_id, timestamps, soft_delete
- **Operations**: id, type, item_id, quantity_change, notes, performed_by, created_at

## Project Structure

```
├── api/                  # API routes and dependencies
├── models/               # SQLAlchemy models
├── schemas/              # Pydantic schemas
├── services/             # Business logic
├── core/                 # Config, security, database
├── alembic/              # Database migrations
├── frontend/             # Web UI
├── tests/                # Unit tests
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
├── Dockerfile
└── docker-compose.yml
```