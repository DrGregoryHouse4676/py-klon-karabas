#!/bin/sh
set -e

python - <<'PY'
import os, time, psycopg2
while True:
  try:
    psycopg2.connect(
      dbname=os.getenv("POSTGRES_DB"),
      user=os.getenv("POSTGRES_USER"),
      password=os.getenv("POSTGRES_PASSWORD"),
      host=os.getenv("POSTGRES_HOST", "db"),
      port=os.getenv("POSTGRES_PORT", "5432"),
    ).close()
    break
  except Exception as e:
    print("DB not ready:", e)
    time.sleep(2)
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput || true
python manage.py seed_theatre || true

if [ "$DJANGO_RUNSERVER" = "1" ]; then
  echo "Starting Django dev server..."
  python manage.py runserver 0.0.0.0:8000
else
  echo "Starting Gunicorn..."
  exec gunicorn theatrebox.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3}
fi
