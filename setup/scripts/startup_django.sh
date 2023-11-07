#!/bin/bash

CERTS='/Users/cosmeaf/Desktop/Projects/django/django_smartmecanico_v006/smart_secure/certs'
GUNICORN='/Users/cosmeaf/Desktop/Projects/django/django_smartmecanico_v006/venv/bin/gunicorn'
CELERY='/Users/cosmeaf/Desktop/Projects/django/django_smartmecanico_v006/venv/bin/celery'

# Matar processos existentes na porta 8000, se houver
echo "Killing any processes running on port 8000..."
fuser -k 8000/tcp
ps -ef | grep 8000 | awk '{print $2}' | xargs sudo kill 9

# Iniciar Gunicorn
#python manage.py runserver 0.0.0.0:8000 &
echo "Starting Gunicorn..."
$GUNICORN core.wsgi:application \
--bind 0.0.0.0:8000 \
--workers 4 \
--certfile=$CERTS/server.pem \
--keyfile=$CERTS/server.key \
--reload --log-level debug &

# Matar instâncias existentes do Celery, se houver
echo "Killing existing Celery processes..."
pkill -9 -f "celery -A core worker"

# Iniciar Celery
echo "Starting Celery..."
$CELERY -A core worker --loglevel=info &
ps -ef | grep celery | awk '{print $2}' | xargs sudo kill 9