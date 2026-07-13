# config/celery.py
# ─────────────────────────────────────────────────────
# This file is the entry point for Celery.
# It tells Celery:
# → where Django settings live
# → where to find tasks (auto-discovers them)
# → which broker to use (Redis)
# ─────────────────────────────────────────────────────

import os
from celery import Celery

# tell Celery which Django settings to use
# same settings.py your Django app uses
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# create the Celery app
# 'config' = name of this Celery instance
app = Celery('config')

# ── CONFIGURATION ────────────────────────────────────
# namespace='CELERY' means all Celery config in settings.py
# must start with CELERY_ prefix
# e.g. CELERY_BROKER_URL, CELERY_RESULT_BACKEND
# ─────────────────────────────────────────────────────
app.config_from_object('django.conf:settings', namespace='CELERY')

# ── AUTO-DISCOVER TASKS ──────────────────────────────
# Celery looks for tasks.py in every INSTALLED_APP
# so you can define tasks close to where they're used
# lib/tasks.py, payments/tasks.py, ecom/tasks.py etc
# ─────────────────────────────────────────────────────
app.autodiscover_tasks()