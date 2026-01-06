# Bestiary Registry - 🐉 Mythical Creature Management System

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)

This project implements **EX1 (FastAPI Backend)** and **EX2 (Streamlit Frontend)**. It is a registry for managing a "Bestiary" of mythical creatures, allowing users to catalogue and view entities across different mythologies.

## Important Links
*   **Backend (Render)**: [https://bestiary-registry.onrender.com](https://bestiary-registry.onrender.com)
*   **Frontend (Streamlit)**: [https://bestiary-registry.streamlit.app](https://bestiary-registry.streamlit.app)
*   **API Documentation**: [https://bestiary-registry.onrender.com/docs](https://bestiary-registry.onrender.com/docs)

## Backend - What Exists
*   **FastAPI** backend with full CRUD support for creatures and classes.
*   **SQLite** used for persistence.
*   Returns standard JSON responses with appropriate HTTP status codes (e.g., 404 for missing resources).

## Frontend - What the User Can Do
*   Implemented using **Streamlit**.
*   View existing registry data fetched from the backend.
*   **CRUD actions**: Fully implemented (Create, Read, Update, Delete).

It features persistent data management, dynamic real-time filtering, automated avatar generation, and a responsive dark-mode UI.

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
  <img src="frontend/pictures/create_creature_pic.png" alt="Details" width="300" style="border: 1px solid #000;">
</p>
*   **Step 3: Confirmation** - Successful registration and feedback.
    
<p align="center">
  <img src="frontend/pictures/create_creature2_pic.png" alt="Confirmation" width="300" style="border: 1px solid #000;">
</p>

### 3. Entity Management (Editing)
Modify existing records with ease, updating attributes like Danger Level, Habitat, or Class as the lore evolves.

<p align="center">
  <img src="frontend/pictures/edit_creature_pic.png" alt="Editing" width="300" style="border: 1px solid #000;">
</p>

### 4. Advanced Filtering
Drill down into the data using powerful multi-select filters for Class, Mythology, and Danger Level ranges.

<p align="center">
  <img src="frontend/pictures/filter_pic.png" alt="Filtering" width="300" style="border: 1px solid #000;">
</p>

### 5. System Settings
Manage global configurations, including the creation and customization of Creature Classes/Categories.

<p align="center">
  <img src="frontend/pictures/settings_pic.png" alt="Settings" width="700">
</p>

---

## Key Features

*   **High-Performance Backend**: Built with **FastAPI**, offering auto-generated Swagger documentation and rapid execution.
*   **Persistent Storage**: Utilizes **SQLite** with **SQLModel** (ORM) for reliable, local data persistence using standard SQL relationships.
*   **Dynamic Frontend**: A "Dark Neon" styled **Streamlit** interface with custom CSS injection for a premium user experience.
*   **Real-Time Exploration**:
    *   **Instant Search**: Filter by name as you type.
    *   **Multi-Faceted Filtering**: Filter by multiple categories simultaneously.
*   **Realm Map**: Visual territory mapping.
*   **Avatars**: Uses DiceBear identicon API. Images are external URLs. No AI/ML is involved.
*   **Testing**: API tests implemented using pytest and FastAPI TestClient.

---

## Technology Stack

| Component | Technologies |
| :--- | :--- |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, SQLModel (Pydantic + SQLAlchemy) |
| **Frontend** | Streamlit, Requests, Custom CSS, `streamlit-keyup` |
| **Database** | SQLite (Local file: `creatures.db`) |
| **Tooling** | `uv` (Package Management), Pytest, Ruff (Linting) |

---

## 📂 Project Structure

```text
EX1_FastAPI_Foundations/
├── backend/
│   ├── app/
│   │   ├── routers/       # API Route modules (creatures, classes)
│   │   ├── services/      # Business logic layer
│   │   ├── models.py      # Database schemas & Pydantic models
│   │   └── db.py          # Database connection & session management
│   ├── tests/             # Backend automated tests
│   ├── main.py            # Application entry point
│   └── pyproject.toml     # Backend dependencies
├── frontend/
│   ├── tests/             # Frontend automated tests
│   ├── pictures/          # Static assets
│   ├── dashboard.py       # Main Application Entry Point
│   ├── sidebar.py         # Navigation component
│   ├── settings.py        # Settings & Configuration page
│   ├── realm_map.py       # Map visualization module
│   └── style.css          # Global visual styling/theming
└── README.md
```

---

## Quick Start Guide

### Prerequisites
*   Python 3.11 or higher
*   `uv` package manager (recommended) or `pip`

### 1. Backend Setup
Initialize the backend environment and start the API server.

```powershell
cd backend
uv sync               # Install dependencies
uv run python main.py # Start server at http://localhost:8000
```

### 2. Frontend Setup
Launch the dashboard interface. (Open a new terminal window).

```powershell
# Ensure you are in the project root or frontend directory
cd backend 
uv run python -m streamlit run ../frontend/dashboard.py
```
*The dashboard will auto-launch at `http://localhost:8501`*

---

## API Documentation

Once the backend is running, full interactive documentation is available:
*   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Testing
API tests are implemented using `pytest` and `FastAPI TestClient`.

Run the full verified test suite:
```powershell
uv run python -m pytest tests/ ../frontend/tests/
# (Run from 'backend' directory)
```
*Tests pass successfully.*

## Code Quality
Uses `ruff` for code formatting and linting.

```powershell
uv run ruff check .
uv run ruff format --check .
```

## 📝 Note
This project serves as a foundation for further course work.