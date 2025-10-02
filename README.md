# MediaManager

A FastAPI-based media management service using SQLModel (SQLAlchemy), with strategy pattern for media processing and robust test/migration setup.

## Features
- Single-table inheritance: all media types stored in one `media` table with a `media_type` discriminator column.
- Strategy pattern: pluggable processors for image/video/media types.
- DTO-ready: use Pydantic/SQLModel models for request/response schemas.
- Robust test isolation: in-memory SQLite, dependency overrides, and explicit table creation in tests.
- Migration scripts for DB schema evolution.
- File upload support for media creation (see API section).

## Quickstart

### 1. Install dependencies
Ensure you have Python 3.9.6 and pipenv installed.
```bash
pipenv sync --dev
```

### 2. Activate environment
```bash
pipenv shell
```

### 3. Run the app
```bash
uvicorn src.main:app --reload
```
App will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 4. Run tests
```bash
pytest -q
```

### 5. Run migration (if upgrading schema)
```bash
python3 scripts/migrate_add_media_type.py
```

### 6. Inspect DB
```bash
python3 scripts/db_inspect.py
```

## Project structure
- `src/database.py` — engine, session, and `get_db` dependency
- `src/main.py` — FastAPI app, router registration (no auto table creation)
- `src/routes/media_routes.py` — models, endpoints, strategy usage
- `src/strategies/media_strategy.py` — strategy pattern for media processing
- `tests/` — pytest tests
- `scripts/` — migration, smoke test, and DB inspection helpers

## API Usage

### Create Media (with file upload)
Send a POST request to `/media/` with `multipart/form-data`:
- `alt_text` (str)
- `extension` (str)
- `media_type` (str, default: "media")
- `file` (UploadFile, optional)

Example using `curl`:
```bash
curl -F "alt_text=Sample" -F "extension=jpg" -F "media_type=media" -F "file=@path/to/file.jpg" http://127.0.0.1:8000/media/
```

### Other endpoints
- `/media/` (GET): List all media
- `/media/{id}` (GET, PUT, DELETE): Retrieve, update, or delete a media item
- `/images/` and `/videos/`: Create image/video media

## Dependency Management
- Unused packages have been removed for clarity and performance.
- Current dependencies (see Pipfile):
  - fastapi ^0.110.0
  - sqlmodel ^0.0.16
  - uvicorn ^0.29.0
  - pytest ^8.2.2 (dev)

## Documentation & Best Practices
- Update `README.md` and architecture diagrams whenever you change models, endpoints, or features.
- See `agents.md` for agent workflow, troubleshooting, and diagram maintenance.

---
For questions or improvements, see `agents.md` or open an issue.
