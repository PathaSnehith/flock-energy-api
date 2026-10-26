# Flock Energy Meter API

A FastAPI service that exposes selected read-only operations from the Urja Meter Ops portal.

## Features

- Search meters by search text.
- Paginate meter search results.
- Retrieve meter energy data.
- Interactive API documentation through Swagger UI.
- Environment-based portal session authentication.
- Basic automated API tests.

## Tech Stack

- Python
- FastAPI
- HTTPX
- Uvicorn
- python-dotenv
- Pytest

## Project Structure

```text
flock-energy-api/
├── app/
│   ├── main.py
│   └── client.py
├── tests/
│   └── test_api.py
├── .env
├── .gitignore
├── openapi.json
├── PROTOCOL.md
└── README.md
```

## Setup

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install fastapi uvicorn httpx python-dotenv pytest
```

### 3. Configure authentication

Create `.env` in the project root:

```env
PORTAL_COOKIE="__Secure-better-auth.session_token=YOUR_CURRENT_SESSION_TOKEN"
```

Replace the placeholder with your own valid session cookie. Never commit `.env` or share the cookie.

### 4. Run the service

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

## API Documentation

After starting the server, open:

- Swagger UI: http://127.0.0.1:8001/docs
- OpenAPI schema: http://127.0.0.1:8001/openapi.json
- Health check: http://127.0.0.1:8001/health

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check service health |
| GET | `/api/meters?search=&page=1` | Search