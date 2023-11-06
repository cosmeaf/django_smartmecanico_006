#!/bin/bash

GUNICORN='/Users/cosmeaf/Desktop/Projects/django/django_smartmecanico_v006/venv/bin/gunicorn'
CELERY='/Users/cosmeaf/Desktop/Projects/django/django_smartmecanico_v006/venv/bin/celery'

# Matar processos existentes na porta 8000, se houver
echo "Killing any processes running on port 8000..."
fuser -k 8000/tcp

# Iniciar Gunicorn
echo "Starting Gunicorn..."
#$GUNICORN core.wsgi:application --bind 0.0.0.0:8000 --workers 4 --log-level=debug &
python manage.py runserver 0.0.0.0:8000 &

# Matar instâncias existentes do Celery, se houver
echo "Killing existing Celery processes..."
pkill -9 -f "celery -A core worker"

# Iniciar Celery
echo "Starting Celery..."
$CELERY -A core worker --loglevel=info &
