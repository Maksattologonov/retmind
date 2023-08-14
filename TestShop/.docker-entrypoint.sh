#!/bin/bash
# Migrate the database first
echo "Migrating the database before starting the server"
export DJANGO_SETTINGS_MODULE="TestShop.settings"
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
# Start Gunicorn processes
echo "Starting Gunicorn."
exec gunicorn TestShop.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3