import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.database import get_db
# Import all models to ensure their tables are created (side-effect import)
from src.routes.media_routes import Media, Image, Video  # noqa: F401

# Create a test engine with a single connection for in-memory SQLite
# Use StaticPool to share the same connection across all sessions

test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestSessionLocal = sessionmaker(bind=test_engine, class_=Session, expire_on_commit=False)

@pytest.fixture(autouse=True)
def create_test_db():
    # Create all tables including Media, Image, and Video
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)

def override_get_db():
    with TestSessionLocal() as session:
        yield session

# Override the get_db dependency used in routes
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_media():
    response = client.post("/media/", json={
        "alt_text": "Sample image",
        "extension": "jpg",
        "url": "http://example.com/image.jpg"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["alt_text"] == "Sample image"
    assert data["extension"] == "jpg"
    assert data["url"] == "http://example.com/image.jpg"
    assert "id" in data

def test_create_image():
    response = client.post("/images/", json={
        "alt_text": "A cat",
        "extension": "png",
        "url": "http://example.com/cat.png"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["alt_text"] == "A cat"
    assert data["extension"] == "png"
    assert data["url"] == "http://example.com/cat.png"
    assert "id" in data

def test_create_video():
    response = client.post("/videos/", json={
        "alt_text": "A dog video",
        "extension": "mp4",
        "url": "http://example.com/dog.mp4"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["alt_text"] == "A dog video"
    assert data["extension"] == "mp4"
    assert data["url"] == "http://example.com/dog.mp4"
    assert "id" in data

def test_get_media():
    client.post("/media/", json={
        "alt_text": "Sample image",
        "extension": "jpg",
        "url": "http://example.com/image.jpg"
    })
    response = client.get("/media/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(m["alt_text"] == "Sample image" for m in data)
