#!/bin/sh
set -e

python manage.py migrate --noinput

if [ "${SEED_DATA:-0}" = "1" ]; then
  python manage.py seed_data --clear
fi

exec gunicorn library_project.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${GUNICORN_WORKERS:-2}"
