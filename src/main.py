from fastapi import FastAPI
from src.database import engine
from src.routes.media_routes import router as media_router

app = FastAPI()

# Register the router
app.include_router(media_router)

# Note: we deliberately do NOT call SQLModel.metadata.create_all(engine) here.
# Creating or migrating production database schema should be done explicitly by
# a migration step or a startup script, not at import time.  This prevents
# test runs from modifying the production SQLite file.
