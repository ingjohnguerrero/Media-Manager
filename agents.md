Agents Guide — MediaManager
===========================

Purpose
-------
This document describes recommended agent responsibilities, conventions, workflows, and troubleshooting tips for working on the MediaManager project (FastAPI + SQLModel). It's written for automated agents, pair-programmers, CI jobs, and newcomers to the repo.

Quick summary
-------------
- Stack: Python 3.9+, FastAPI, SQLModel (SQLAlchemy under the hood), PyTest, TestClient.
- Repo layout (relevant files):
  - `src/database.py` — engine & session factory, concrete `get_db` dependency for session injection
  - `src/main.py` — FastAPI app, router registration (no auto table creation)
  - `src/routes/media_routes.py` — models and HTTP routes
  - `src/strategies/media_strategy.py` — strategy pattern for media processing
  - `tests/` — pytest tests (e.g. `tests/routes/test_media_routes.py`)
  - `scripts/` — migration, smoke test, and DB inspection helpers

Single-table inheritance & strategy pattern
------------------------------------------
- Only one table: `media` (see `src/routes/media_routes.py`).
- `Media` is the ORM model with a `media_type` discriminator column.
- `Image` and `Video` are non-table SQLModel models used for request validation.
- Endpoints `/images/` and `/videos/` create `Media` rows with `media_type` set to "image" or "video".
- Strategy pattern: `src/strategies/media_strategy.py` registers processors for each media type; endpoints call the processor before saving.

Testing / DB conventions
------------------------
- Tests use `fastapi.testclient.TestClient` to exercise the app synchronously.
- Tests provide an isolated in-memory SQLite database using:
  - `sqlite:///:memory:`
  - `sqlalchemy.pool.StaticPool`
  - `connect_args={"check_same_thread": False}`
- The test fixture creates all tables via `SQLModel.metadata.create_all(test_engine)` after importing all models.
- Tests override the app session dependency with `app.dependency_overrides[get_db] = override_get_db` to point to the test engine/session factory.
- Always import models for side-effect in tests so SQLModel metadata is complete.

Dependency override pattern
---------------------------
- Use a concrete `get_db()` dependency in routes (not a factory).
- In tests, override with a function that yields sessions bound to the test engine.
- Example:
```python
app.dependency_overrides[get_db] = override_get_db
```

DB migration and schema management
----------------------------------
- Do not call `SQLModel.metadata.create_all(engine)` at import time in production code.
- Use explicit migration scripts (see `scripts/migrate_add_media_type.py`) to add new columns.
- Always back up the production DB before running migrations.
- Inspect DB schema with `scripts/db_inspect.py`.

Common pitfalls and how to fix them
----------------------------------
1. `sqlite3.OperationalError: table media has no column named media_type`
   - Cause: production DB was created before the model included `media_type`.
   - Fix: run migration script to add the column.

2. Pydantic v2 from_orm() error: `You must set the config attribute from_attributes=True to use from_orm`
   - Cause: DTO class does not have the correct config for Pydantic v2.
   - Fix: In your DTO, add:
     ```python
     class MediaReadDTO(BaseModel):
         ...
         model_config = {"from_attributes": True}
     ```
   - Remove any old `Config` class with `orm_mode=True` (used in v1).
   - For Pydantic v1, use `class Config: orm_mode = True`. For v2, use `model_config = {"from_attributes": True}`.

3. Tests touching production DB
   - Cause: auto table creation at import time.
   - Fix: remove `SQLModel.metadata.create_all(engine)` from import-time code; create tables only in test fixtures or migration scripts.

4. Dependency override not working
   - Cause: using a factory or lambda instead of a concrete function.
   - Fix: use a concrete `get_db()` dependency and override it directly.

5. SQLModel metadata incomplete in tests
   - Cause: not importing all models before creating tables.
   - Fix: import all models for side-effect in test files.

Agent responsibilities (suggested roles)
----------------------------------------
- test-runner agent
  - Runs `pytest` on commits/PRs.
  - Reports failures and attaches logs.
- db/infra agent
  - Reviews DB engine and session creation.
  - Verifies table creation timing and migrations.
- code-style agent
  - Runs linters (flake8/ruff) and type checks (mypy) if configured.
- developer assistant agent
  - Makes small PRs to fix failing tests, run tests locally, and document changes.

How an agent should add a new route or model (TDD workflow)
---------------------------------------------------------
1. Write a failing test in `tests/` that describes the desired API behavior.
2. Run `pytest -q` to see the failing test.
3. Implement the minimal route/model in `src/routes/` and wire into `src/main.py`.
4. Ensure DB model changes do not cause table creation timing issues — import models before calling `SQLModel.metadata.create_all(engine)`.
5. Re-run tests and iterate until green.

Small templates
---------------
- New test file template (pytest):
```python
from fastapi.testclient import TestClient
from src.main import app
client = TestClient(app)

def test_my_feature():
    response = client.post('/myroute', json={...})
    assert response.status_code == 201
```

- New model template:
```python
from sqlmodel import SQLModel, Field
from typing import Optional

class Media(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    alt_text: str
    extension: str
    url: str
    media_type: str = Field(default="media")
```

Debugging tips
--------------
- Print which tables are registered in metadata:
```python
from sqlmodel import SQLModel
print([t for t in SQLModel.metadata.tables])
```
- Enable SQL echo for a engine to see SQL statements:
```python
create_engine("sqlite:///./my.db", echo=True)
```
- When you see pickling / deepcopy errors, simplify model fields and check for non-pickleable defaults.

CI considerations
-----------------
- Ensure `pipenv sync --dev` or an equivalent `requirements.txt` installation step runs during CI setup.
- Run `pytest -q` and fail fast on errors.
- Cache `.pytest_cache` and virtualenv artifacts if helpful.

Maintaining Mermaid Diagrams
---------------------------
- Mermaid diagrams (class, ERD, sequence) are located in `README.md` under the "Architecture Diagrams" section.
- Whenever you change models, DTOs, database schema, or API routes, update the corresponding Mermaid diagrams to reflect the new structure and flow.
- Use clear Mermaid syntax and keep diagrams concise but accurate. See the current diagrams in `README.md` for examples.
- After major refactors, review all diagrams for correctness and completeness.
- If you add new features (e.g., new media types, new endpoints), add/update diagrams to illustrate the changes.
- This helps keep documentation useful for onboarding, troubleshooting, and architectural reviews.

Appendix: useful commands
------------------------
- Sync dev environment: `pipenv sync --dev`
- Install dev deps: `pipenv install --dev`
- Run tests: `pytest -q`
- Run single test: `pytest tests/routes/test_media_routes.py::test_create_media -q`
- Start app (for manual testing):
```bash
pipenv shell
uvicorn src.main:app --reload
```
- Run migration to add missing columns:
```bash
python3 scripts/migrate_add_media_type.py
```
- Inspect DB schema:
```bash
python3 scripts/db_inspect.py
```

Contact & follow-ups
--------------------
- If you want, I can also add a `README.md` with a condensed developer setup and/or CI YAML for GitHub Actions to run the test suite.

---

This `agents.md` is a living doc — keep it updated with new recurring errors and best practices as the project evolves.
