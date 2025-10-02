"""
Shared FastAPI dependencies for MediaManager.
Add reusable dependency functions here.
"""
from context.config import settings
from fastapi import Depends

def get_settings():
    return settings

# Example: add more dependencies as needed

