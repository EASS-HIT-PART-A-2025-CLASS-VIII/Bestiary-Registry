# Bestiary Registry — Mythical Creature Management System (EX1–EX3)

A full-stack course project that evolves across three exercises:

- **EX1**: Dockerized **FastAPI** backend (clean layering + tests)
- **EX2**: **Streamlit** frontend that talks **only** to the main backend
- **EX3**: Multi-service setup via **Docker Compose** (main backend + PostgreSQL + AI service + Redis/worker + frontend)

---

## What you can do

- Manage a registry (“bestiary”) of mythical creatures with **CRUD** operations.
- Manage supporting entities such as **classes/categories** and **tags**.
- (EX3) Trigger **AI image generation** for a creature via the main backend (the frontend never calls the AI service directly).
- (EX3) Use a real database (**PostgreSQL**) with **migrations** and **seed data**.

---

## Important links

- **Frontend (local)**: http://localhost:8501  
- **Backend (local)**: http://localhost:8000  
- **API docs (local)**: http://localhost:8000/docs  
- **Health check (local)**: http://localhost:8000/health  

> If you deployed (Render / Streamlit Cloud), add your deployed links here.

---

## Architecture (EX3)

**Service boundaries (required):**
- `frontend` → **main-backend only**
- `main-backend` → `db` (PostgreSQL) + `ai-service` + `redis` (worker queue)

**Services in `compose.yaml`:**
- **main-backend** (FastAPI): public API for the UI, orchestrates DB + AI calls
- **db** (PostgreSQL): persistent storage
- **redis**: queue backend for background jobs
- **worker**: async job runner (image generation, etc.)
- **ai-service** (FastAPI): AI image generation HTTP API
- **frontend** (Streamlit): UI

### Configuration (Environment Variables)

Recommended settings for `.env`:

| Variable | Description | Default | Required? |
| :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google Gemini API key for image generation. | `change_me` | Yes (unless Mock Mode) |
| `MOCK_MODE` | Set to `1` or `true` to skip real API calls. | `0` | No |
| `SECRET_KEY` | Secret for JWT authentication security. | `change_me...` | Yes |
| `POSTGRES_USER` | Database user. | `postgres` | Yes (in docker) |
| `POSTGRES_PASSWORD` | Database password. | `postgres` | Yes (in docker) |
| `POSTGRES_DB` | Database name. | `creatures` | Yes (in docker) |

<!-- PROTECTED:IMAGE_FLOW:BEGIN -->
**Flow**:
1.  User creates a creature via **Frontend**.
2.  **Frontend** POSTs to **Main Backend**.
3.  **Main Backend** saves to **DB** (status: `pending`) and enqueues a job in **Redis**.
4.  **Worker** picks up the job, requests image from **AI Service**, saves the result to shared volume, and updates **DB**.
<!-- PROTECTED:IMAGE_FLOW:END -->

---

## Application Showcase

### 1. The Dashboard
The central command center for monitoring all registered entities. Features real-time metrics, a responsive data grid, and quick actions. 

<p align="center">
<img src="frontend/pictures/dashboard_pic.png" alt="dashboard preview" width="700" >
</p>

### 2. Summoning New Entities
A streamlined workflow for adding new creatures to the registry.
*   **Step 1: Initiation** - Launching the summon dialog.
    
<p align="center">
  <img src="frontend/pictures/create_creature_full_screen_pic.png" alt="Initiation" width="700">
</p>

*   **Step 2: Details** - Filling in creature attributes (Class, Mythology, Danger Level).

<p align="center">
  <kbd>
    <img src="frontend/pictures/create_creature2_pic.png" alt="Confirmation" width="300" >
  </kbd>
</p>

*   **Step 3: Creation** - Pressing the 'Summon Entity' button creates a new creature and adds it into the registry.


### 3. Entity Management (Editing)
Modify existing records with ease, updating attributes like Danger Level, Habitat, or Class as the lore evolves.

<p align="center">
  <kbd>
    <img src="frontend/pictures/edit_creature_pic.png" alt="Editing" width="300" >
  </kbd>
</p>

### 4. Advanced Filtering
Drill down into the data using powerful multi-select filters for Class, Mythology, and Danger Level ranges.

<p align="center">
  <kbd>
    <img src="frontend/pictures/filter_pic.png" alt="Filtering" width="300" >
  </kbd>
</p>

### 5. System Settings
Manage global configurations, including the creation and customization of Creature Classes/Categories.

<p align="center">
  <img src="frontend/pictures/settings_pic.png" alt="Settings" width="700">
</p>

---

## Key features

- **FastAPI backend** with OpenAPI/Swagger docs
- **SQLModel** models + repository/service layering
- **Alembic migrations** (EX3)
- **Seed script** for deterministic local/demo data (EX3)
- **Automated tests** with `pytest` + `FastAPI TestClient`
- **Ruff** formatting + linting
- **Docker Compose**: one command to bring up the full stack

---

## Tech stack

| Component | Technologies |
| --- | --- |
| Backend | Python 3.13+, FastAPI, Uvicorn, SQLModel |
| DB (EX3) | PostgreSQL, Alembic (migrations) |
| Worker/Queue (EX3) | Redis, ARQ worker |
| AI service (EX3) | FastAPI (HTTP), external AI provider integration (configurable) |
| Frontend | Streamlit, Requests/HTTPX, custom UI styling |
| Tooling | `uv`, Pytest, Ruff, GitHub Actions (CI), Schemathesis (API checks) |

---

## Project structure (high level)

```text
.
├── backend/
│   ├── app/                     # Main application code
│   │   ├── routers/             # API Endpoints
│   │   ├── services/            # Business logic
│   │   └── models.py            # Database schemas
│   ├── tests/                   # Backend tests
│   └── alembic/                 # Database migrations
├── ai-service/                  # Independent AI image generation service
├── frontend/                    # Streamlit Dashboard code
├── compose.yaml                 # Docker Compose configuration
└── scripts/                     # Helper utilities
```

## Quick start (recommended): Docker Compose (EX3)

### Prerequisites
- Docker Desktop (or Docker Engine) with Compose
- (Optional) `uv` + Python 3.13+ if you also want to run things outside Docker

### 1) Configure environment
Create a local `.env` file from the template:

```powershell
cp .env.example .env
# Fill in the required values in .env (only what your project actually uses).
```

### 2) Start the full stack
From the repository root:

```powershell
docker compose up --build
```

Then open:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000/docs

---

## Setup & seeding (EX3)

### Apply migrations
```powershell
docker compose exec main-backend uv run alembic upgrade head
# If your backend service name in compose.yaml is not main-backend, replace it accordingly.
```

### Seed data
```powershell
docker compose exec main-backend uv run python -m app.seed
# If your backend service name in compose.yaml is not main-backend, replace it accordingly.
```

---

## Local development (without Docker)

### Backend
```powershell
cd backend
uv sync
uv run uvicorn app.app:app --reload --port 8000
```

### Frontend
```powershell
# from repo root
cd backend
uv run streamlit run ../frontend/dashboard.py
```

---

---

## API Examples

Quickly test the API using `curl`:

**1. Create a Creature**
```bash
curl -X POST "http://localhost:8000/creatures/" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Phoenix",
           "creature_type": "Bird",
           "mythology": "Greek",
           "danger_level": 8,
           "habitat": "Volcano"
         }'
```

**2. List Creatures**
```bash
curl "http://localhost:8000/creatures/"
```

---

## Tests

Run backend tests:

```powershell
cd backend
uv run python -m pytest
```

---

## Code quality (Ruff)

From repo root:

```powershell
uv run ruff format --check .
uv run ruff check .
```

To auto-format:

```powershell
uv run ruff format .
```


---

## Troubleshooting

### Top Issues

1.  **"Port already in use"**
    -   Stop other containers: `docker compose down` or check if local modules are running.
    -   Host ports `8000` (Backend) and `8501` (Frontend) must be free.

2.  **"Image generation failed"**
    -   Check `ai-service` logs: `docker compose logs ai-service`
    -   Verify `GEMINI_API_KEY` is valid in `.env`.
    -   Ensure `MOCK_MODE=0` if you want real images.

3.  **"Database connection failed"**
    -   Wait 10-15 seconds for Postgres to initialize on first run.
    -   Check logs: `docker compose logs db`