FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Install dependencies first (better layer caching)
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

# Copy application code
COPY . .

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
