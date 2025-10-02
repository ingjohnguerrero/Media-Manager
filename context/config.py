"""
Centralized configuration for MediaManager.
Add environment variables, feature flags, and settings here.
"""
import os

class Settings:
    ENV: str = os.getenv("MEDIAMANAGER_ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///mediamanager.db")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    # Add more settings as needed

settings = Settings()

