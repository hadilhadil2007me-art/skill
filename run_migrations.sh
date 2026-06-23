#!/usr/bin/env bash
set -e
echo "Running Alembic migrations..."
alembic upgrade head
echo "Migrations applied."
