#!/usr/bin/env bash
set -e

# Run database migrations before starting the app
echo "Running database migrations..."
alembic upgrade head

echo "Starting application..."
exec fastapi run simple_todo/app.py --host 0.0.0.0 --port 8000
