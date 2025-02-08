#!/bin/bash
docker compose exec fastapi python -m alembic revision --autogenerate -m "$1"
docker compose exec fastapi python -m alembic upgrade head 