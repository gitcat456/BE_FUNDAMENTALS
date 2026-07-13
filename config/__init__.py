# config/__init__.py
# ─────────────────────────────────────────────────────
# This makes Celery load automatically when Django starts.
# Without this, you'd have to import Celery manually
# in every file that uses it.
# ─────────────────────────────────────────────────────

from .celery import app as celery_app

__all__ = ('celery_app',)