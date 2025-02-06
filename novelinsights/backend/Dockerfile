# novelinsights/backend/Dockerfile
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup"

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies and Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        git \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get purge -y --auto-remove build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $PYSETUP_PATH

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY . .

# Development stage
FROM base AS dev
RUN poetry install --with dev

# Create an entrypoint script
RUN echo '#!/bin/bash\n\
alembic upgrade head\n\
uvicorn novelinsights.main:app --host 0.0.0.0 --port 8000 --reload\n\
' > /entrypoint.sh \
    && chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]

# Production stage
FROM base AS prod
RUN poetry install --without dev

CMD ["poetry", "run", "gunicorn", "novelinsights.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]