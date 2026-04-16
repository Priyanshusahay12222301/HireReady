import os
import sys

# Ensure backend package imports resolve when running in Vercel Python runtime.
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Vercel serverless filesystem is read-only except /tmp.
os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/hireready_dev.sqlite3")

from app import create_app  # noqa: E402

app = create_app("production")
