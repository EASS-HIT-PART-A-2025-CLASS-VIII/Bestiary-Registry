# Bestiary Registry - FastAPI & Streamlit Project

A full-stack application for managing a catalogue of mythical creatures. This project demonstrates a modern Python web stack with FastAPI for the backend and Streamlit for the frontend, featuring persistent storage and AI-generated avatars.

## Key Features
*   **FastAPI Backend**: Robust REST API with CRUD operations.
*   **Persistent Database**: SQLite database (`creatures.db`) using SQLModel (ORM).
*   **Interactive Dashboard**: A Streamlit UI (`dashboard.py`) for managing creatures.
*   **AI Avatars**: Automatic avatar generation using Robohash (Monsters Set) for every creature.
*   **Dynamic UI**: Real-time updates and live editing/deleting.

## Technology Stack
*   **Language**: Python 3.11+
*   **Backend**: FastAPI, Uvicorn, SQLModel (Pydantic + SQLAlchemy).
*   **Frontend**: Streamlit, Requests.
*   **Tools**: `uv` (dependency management), Pytest, Docker (optional).

## Project Structure
```
.
├── backend/
│   ├── app/
│   │   ├── app.py          # Main FastAPI application & Database logic
│   │   └── models.py       # SQLModel database schemas
│   ├── main.py             # Entry point (runs Uvicorn)
│   ├── creatures.http      # REST Client test file
│   └── creatures.db        # SQLite Database file (auto-generated)
├── frontend/
│   └── dashboard.py        # Streamlit Dashboard UI
├── tests/                  # Automated tests
├── pyproject.toml          # Dependencies
└── README.md               # This file
```

## Quick Start

### 1. Backend Setup
Navigate to the `backend` directory and install dependencies:

```powershell
cd backend
uv sync
```

Run the backend server:
```powershell
uv run python main.py
```
*The server will start at `http://localhost:8000`*

### 2. Frontend Setup
Open a new terminal, navigate to the `frontend` directory (or run from root):

```powershell
# From project root
uv run streamlit run frontend/dashboard.py
```
*The dashboard will open automatically in your browser at `http://localhost:8501`*

## API Documentation
Once the backend is running, you can explore the auto-generated docs:
*   **Swagger UI**: http://localhost:8000/docs
*   **ReDoc**: http://localhost:8000/redoc

## Running Tests
To run the automated test suite:

```powershell
uv run pytest
```

## Running with Docker (Optional)
If you prefer using Docker to run the backend:

1.  **Build the Image**:
    ```powershell
    cd backend
    docker build -t creatures-backend .
    ```

2.  **Run the Container**:
    ```powershell
    docker run -p 8000:8000 creatures-backend
    ```
    *The API will be available at `http://localhost:8000`*

## Notes
*   **Database**: The project uses a local SQLite file. If you delete `backend/creatures.db`, the application will create a fresh, empty one on the next restart.
*   **Avatars**: Images are generated dynamically. If the external avatar service is down, the backend handles the fallback.