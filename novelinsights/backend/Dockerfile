# novelinsights/backend/app/Dockerfile
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Add Poetry and virtual environment paths to PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install system dependencies and Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

# Copy only poetry files first to leverage cache
COPY pyproject.toml poetry.lock ./

# Development stage (includes all dependencies)
FROM base AS dev
RUN poetry install --no-root
COPY . .
CMD ["poetry", "run", "uvicorn", "novelinsights.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage (excludes development dependencies)
FROM base AS prod
RUN poetry install --no-dev --no-root
COPY . .
CMD ["poetry", "run", "gunicorn", "novelinsights.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]