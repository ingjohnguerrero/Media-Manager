import sys
from pathlib import Path

# Ensure the project root is on sys.path so imports like `from src.main import app` work
# This helps IDE test runners (PyCharm) that sometimes don't add the project root to PYTHONPATH.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

