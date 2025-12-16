#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --noinput --ignore admin

# Only run migrations if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
    python manage.py migrate --noinput
fi
