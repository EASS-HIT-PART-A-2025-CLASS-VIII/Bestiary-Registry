# EX1 — Creatures Backend Service

Short description
-----------------
Core backend microservice for the Creatures Catalogue domain. This example app demonstrates a small REST API for managing mythical creatures using FastAPI. Persistence is in-memory for EX1 (no database required).

Key technologies
----------------
- FastAPI — web framework
- Pydantic / SQLModel — models and validation
- pytest — automated tests
- uv — environment & dependency commands

Project layout
--------------
```
.
├─ app/
│  ├─ app.py          # FastAPI application (CRUD for /creatures)
│  └─ models.py       # SQLModel Creature definition
├─ tests/
│  └─ test_creatures.py
├─ main.py            # Entry point — runs uvicorn with app.app:app
├─ creatures.http     # HTTP playground (REST Client requests)
├─ Dockerfile         # Optional containerization
└─ pyproject.toml     # Project metadata and dependencies
```

Prerequisites
-------------
- Python 3.11+
- `uv` (optional helper used by this project)

Quick start (PowerShell)
------------------------
From the project root:

Create virtual environment:

```powershell
uv venv
```

Activate the venv (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies from `pyproject.toml`:

```powershell
uv sync
```

Run the application (recommended):

```powershell
uv run python main.py
```
# or when venv is active:
```
python main.py
```

Run with uvicorn directly:

```powershell
uv run uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload
```

Useful URLs
-----------
- Base URL: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

API overview
------------
All endpoints operate on a single resource: `Creature` (stored in-memory with an auto-incrementing id).

Endpoints
---------
- `POST /creatures/` — create a creature. Request body: `CreatureCreate`.
- `GET /creatures/` — list all creatures.
- `PUT /creatures/{id}` — replace/update a creature (full update).
- `DELETE /creatures/{id}` — delete a creature.

Example data
------------
Request (`CreatureCreate`):

```json
{
	"name": "Dragon",
	"mythology": "Fantasy",
	"creature_type": "Fire",
	"danger_level": 10
}
```

Response (`CreatureRead`):

```json
{
	"id": 1,
	"name": "Dragon",
	"mythology": "Fantasy",
	"creature_type": "Fire",
	"danger_level": 10
}
```

Tests
-----
This project uses `pytest` with FastAPI's `TestClient`.

> Note: the example `DELETE` request uses `/creatures/1`, which deletes only the creature with ID `1`.
> If you create a different creature, replace `1` with the actual `id` returned in the POST response.

Run tests:

```powershell
uv run python -m pytest
# or when venv is active:
python -m pytest
```

HTTP playground
--------------
Open `creatures.http` in VS Code (REST Client extension) and use the example requests. Ensure the API is running before sending requests.

Notes & next steps
------------------
- Storage is in-memory for EX1. Future exercises may replace it with SQLModel + SQLite.
- The code and tests are structured to make adding a repository layer and migrations straightforward.

Want changes?
-------------
- I kept the README in English. If you prefer Hebrew, I can produce an equivalent Hebrew version instead.
- I can also make the headings more compact, add badges, or update `creatures.http` with fresh examples — tell me which you'd like.