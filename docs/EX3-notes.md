# EX3 Notes

## Orchestration Flow
The architecture consists of the following services Orchestrated via `compose.yaml`:

1. **Frontend (`frontend`)**: Streamlit application served on port 8501. It communicates *only* with the `main-backend` service via HTTP (`BACKEND_URL`).
2. **Main Backend (`main-backend`)**: FastAPI application on port 8000. It handles API requests, business logic, and orchestrates calls to dependencies.
   - Connects to **PostgreSQL (`db`)** for persistent storage of Creatures, Users, and Tags.
   - Connects to **Redis (`redis`)** for async task queuing and idempotency keys.
   - Connects to **AI Service (`ai-service`)** for generating creature avatars.
3. **AI Service (`ai-service`)**: Independent FastAPI microservice. Generates artifacts (avatars) on demand.
4. **Worker (`worker`)**: Background Python worker (Arq) consuming tasks from Redis.
5. **DB (`db`)**: PostgreSQL 15 database.
6. **Redis (`redis`)**: Redis message broker/cache.

**Dependencies**:
- `main-backend` depends on `db`, `redis`, `ai-service`.
- `worker` depends on `redis`, `db`.
- `frontend` depends on `main-backend`.

## Security Baseline - Session 11
We implemented a security baseline including:
- **Hashing**: Passwords are hashed using `bcrypt` (via `passlib`) before storage in the `User` table.
- **JWT**: Stateless authentication using JSON Web Tokens.
- **Role-Based Access**: The endpoint `POST /admin/rotate-keys` enforces `role="admin"` check.

### Rotation Instructions
To rotate secrets (e.g. `SECRET_KEY` or API keys):
1. Update the `SECRET_KEY` environment variable in `compose.yaml` (or `.env`).
2. Redeploy services: `docker compose up -d --build`.
3. Invalidate existing sessions: Since we use stateless JWTs, changing the key invalidates all existing tokens immediately. Users must re-login.
4. (Optional) For database credentials, update `POSTGRES_PASSWORD` in `compose.yaml` and update `DATABASE_URL` in backend/worker services.

## Async & Idempotency Trace (Session 09)
Below is a trace of the `refresh.py` script running with bounded concurrency and Redis-backed idempotency.

```log
INFO:__main__:Item 0 processing...
INFO:__main__:Item 1 processing...
INFO:__main__:Item 2 processing...
INFO:__main__:Item 3 processing...
INFO:__main__:Item 4 processing...
INFO:__main__:Item 0 processed successfully.
INFO:__main__:Item 5 processing...
...
INFO:__main__:Item 0 already processed. Skipping.
```
*(Simulated trace based on logic implement in scripts/refresh.py)*
