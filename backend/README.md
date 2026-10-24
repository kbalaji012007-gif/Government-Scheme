# RuralConnect Karnataka - FastAPI Backend

The backend engine for **RuralConnect Karnataka**, an accessibility-first welfare scheme discovery platform for rural residents across Karnataka.

---

## Tech Stack & Architecture

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Server:** Uvicorn
- **Validation & Settings:** Pydantic v2 & Pydantic-Settings
- **Database Driver:** PyMongo (with transparent in-process fallback via mongomock for isolated development and offline testing)
- **Security:** Password hashing with `bcrypt`, signed JWT access tokens via `pyjwt`
- **Testing:** `pytest`, `pytest-asyncio`, and `httpx`

---

## Directory Structure

```text
backend/
├── app/
│   ├── main.py              # Application lifecycle, CORS, route registration
│   ├── core/
│   │   ├── config.py        # Environment settings (Pydantic Settings)
│   │   └── security.py      # bcrypt password hashing & JWT token management
│   ├── db/
│   │   └── mongodb.py       # MongoDB client, ping, auto-mock fallback, indexes
│   ├── models/              # Internal domain entities
│   ├── schemas/             # Pydantic v2 request/response contracts
│   ├── repositories/        # MongoDB data access layer
│   ├── services/            # Business logic (eligibility rule engine, auth)
│   ├── routers/             # API v1 route handlers
│   └── utils/               # Pagination and formatting helpers
├── scripts/
│   └── seed_data.py         # Safe idempotent database seed script
├── tests/                   # Automated pytest suite
├── .env.example             # Example environment configuration
├── requirements.txt         # Pinned production and test dependencies
└── README.md
```

---

## Prerequisites

- Python 3.11 or higher (Python 3.12 recommended)
- MongoDB Community Server (optional: if local MongoDB daemon is not running on port 27017, the application automatically uses an in-process database so all APIs and tests work out-of-the-box).

---

## Setup & Running (Windows PowerShell)

```powershell
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
pip install -r requirements.txt

# 5. Populate sample data (optional, auto-seeds on first startup)
python scripts/seed_data.py

# 6. Start the FastAPI development server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## API Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/health` | Service and database health check |
| `GET` | `/api/v1/categories` | Welfare scheme categories with counts |
| `GET` | `/api/v1/schemes` | Filterable and searchable scheme listing |
| `GET` | `/api/v1/schemes/{id}` | Detailed scheme guidelines, benefits, rules |
| `GET` | `/api/v1/schemes/{id}/documents` | Required document checklist |
| `GET` | `/api/v1/schemes/{id}/eligibility` | Dynamic questionnaire configuration |
| `POST` | `/api/v1/schemes/{id}/check-eligibility` | Evaluates answers against criteria |
| `GET` | `/api/v1/centers` | Service centre directory (Grama One, etc.) |
| `GET` | `/api/v1/centers/{id}` | Detailed centre contacts and directions |
| `POST` | `/api/v1/auth/register` | Citizen registration |
| `POST` | `/api/v1/auth/login` | Citizen login |
| `GET` | `/api/v1/auth/me` | Authenticated profile (requires Bearer token) |

Swagger interactive documentation is available at: `http://127.0.0.1:8000/docs`

---

## Running Backend Tests

```powershell
.\.venv\Scripts\pytest.exe -v tests
```
