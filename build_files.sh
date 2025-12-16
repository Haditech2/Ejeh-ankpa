#!/bin/bash
pip install -r requirements.txt

# Set DATABASE_URL for build if available in environment
export DATABASE_URL="${DATABASE_URL:-}"

python manage.py collectstatic --noinput --ignore admin

# Only run migrations if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
    python manage.py migrate --noinput
fi
