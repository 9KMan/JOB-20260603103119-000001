# Inventory & Operations System

A full-stack inventory management system built with FastAPI, PostgreSQL, and a responsive frontend.

## Features

- **Authentication**: JWT-based user authentication with bcrypt password hashing
- **Inventory Management**: Full CRUD operations for inventory items with SKU, RFID support
- **Operations Tracking**: Track inventory movements (ADD, REMOVE, ADJUST, AUDIT)
- **Responsive UI**: Modern, mobile-friendly interface
- **RESTful API**: Versioned API endpoints (/api/v1/...)


## Business Problem Solved

Warehouses and operations teams lose thousands per year due to manual inventory tracking errors, stock discrepancies, and blind spots in supply chain visibility. A retail or logistics business managing inventory by spreadsheet or intuition cannot scale reliably — items go missing, orders ship incomplete, and reorder points get guessed rather than calculated.

**Who this solves it for:**
- Warehouse managers who need real-time stock visibility across locations
- Operations teams tracking RFID-tagged assets as they move through receiving, storage, and fulfillment
- Small-to-medium businesses replacing manual counts with automated audit trails

**What you get:**
- Accurate, real-time inventory records — every ADD, REMOVE, ADJUST, or AUDIT operation is logged with timestamp, user, and notes
- RFID-enabled tracking so physical items map directly to digital records
- Soft-delete safety net: nothing is permanently lost, records can be recovered
- Fast audit: inspectors can run an AUDIT operation and immediately see discrepancies against expected quantities
- SKU uniqueness enforcement prevents duplicate items from entering the system

**Technical delivery:**
- REST API (FastAPI) with JWT-authenticated endpoints — auditors, managers, and systems all have controlled access
- PostgreSQL backend with proper indexes on foreign keys and high-cardinality columns for fast queries at scale
- Responsive SPA frontend so teams can manage inventory from desktop or mobile
- Docker Compose for one-command local dev and production deployment

This system turns inventory from guesswork into a verifiable, auditable process.
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