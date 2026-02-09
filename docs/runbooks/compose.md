# Docker Compose Runbook

## Launching the Stack
To start the entire EX3 stack (Frontend, Backend, AI Service, DB, Redis, Worker):

```bash
# In the root project directory (where compose.yaml is):
docker compose up --build
```

This will build the images and start the services.
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **AI Service**: Internal only (or exposed on 8000 if port mapped, but backend uses internal `ai-service:8000`)

## Verifying Health
Check the status of containers:
```bash
docker compose ps
```
All services should be `healthy` (where healthchecks are defined).

You can check the backend health endpoint:
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

## Verifying Rate Limits
The backend uses Redis for rate limiting (if enabled) or headers for API usage. To verify headers are present:

1. **Endpoint**: `GET /creatures`
2. **Header to check**: `X-RateLimit-Limit` or similar (depending on `slowapi` or implementation). If strictly verifying *connectivity* to Redis, check logs or headers.
   *Note: If explicit rate limiting middleware is running, headers will appear.*

Example verification command:
```bash
curl -v http://localhost:8000/creatures 2>&1 | grep "X-RateLimit"
```
*(If no rate limit is configured, this grep might come empty, but the request should succeed 200 OK).*

## Verifying Secure Cloud Key
To confirm that the `GEMINI_API_KEY` is injected securely *only* into the AI service:

1. Start the stack:
   ```bash
   docker compose up -d
   ```
2. Run the verification check:
   ```bash
   docker compose exec ai-service env | grep GEMINI_API_KEY
   ```
   *Expected Output*: `GEMINI_API_KEY=...` (your key)

3. Verify it is **NOT** in the backend:
   ```bash
   docker compose exec main-backend env | grep GEMINI_API_KEY
   ```
   *Expected Output*: (Empty)

## Running Tests in CI
The CI pipeline runs:
1. `ruff check .` (Linting)
2. `pytest` (Unit/Integration tests)
3. `schemathesis run http://localhost:8000/openapi.json` (API Fuzzing)

To run locally:
```bash
cd backend
uv run pytest
uv run schemathesis run http://localhost:8000/openapi.json
```
