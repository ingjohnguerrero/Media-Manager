from sqlmodel import SQLModel, create_engine, Session

# Create the production engine (file-based SQLite)
engine = create_engine("sqlite:///./mediamanager.db", echo=True)
# Don't create tables here - will be done after all models are imported

def get_session(engine_param=None):
    def _get_session():
        # Use the passed engine or fall back to the default engine
        session_engine = engine_param or engine
        with Session(session_engine) as session:
            yield session
    return _get_session

# Concrete dependency used by routes; tests can override this exact callable
def get_db():
    with Session(engine) as session:
        yield session
