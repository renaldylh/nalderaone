#!/bin/bash
set -e

# 1. Restore the SQLite database from Cloudflare R2 if it exists and local DB is missing
if [ -n "$LITESTREAM_BUCKET" ]; then
    echo "Checking for database restore from Cloudflare R2..."
    litestream restore -if-db-not-exists -if-replica-exists -config /app/litestream.yml /app/db.sqlite3
else
    echo "LITESTREAM_BUCKET not set. Skipping database restore."
fi

# 2. Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# 3. Start the background task processor in the background
echo "Starting background task processor..."
python manage.py process_tasks &

# 4. Start Gunicorn (wrapped with Litestream if configured)
if [ -n "$LITESTREAM_BUCKET" ]; then
    echo "Starting Gunicorn with Litestream replication..."
    exec litestream replicate -config /app/litestream.yml -- exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 2
else
    echo "Starting Gunicorn without replication..."
    exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 2
fi
