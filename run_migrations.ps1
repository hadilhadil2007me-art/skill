Write-Host "Running Alembic migrations..."
& alembic upgrade head
Write-Host "Migrations applied."
