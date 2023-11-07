# smart_secure/management/commands/django_startup.py

from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess
import os

class Command(BaseCommand):
    help = 'Start the Django project services'

    def handle(self, *args, **options):
        # Caminho para o diretório de certificados e executáveis
        certs_dir = os.path.join(settings.BASE_DIR, 'smart_secure', 'certs')
        gunicorn_path = os.path.join(settings.BASE_DIR, 'venv', 'bin', 'gunicorn')
        celery_path = os.path.join(settings.BASE_DIR, 'venv', 'bin', 'celery')


        # Encerrar processos existentes que podem estar utilizando a porta 8000
        self.stdout.write("Killing any processes running on port 8000...")
        subprocess.run(['fuser', '-k', '8000/tcp'])

        # Iniciar Gunicorn
        self.stdout.write("Starting Gunicorn...")
        subprocess.Popen([
            gunicorn_path, 'core.wsgi:application',
            '--bind', '0.0.0.0:8000',
            '--workers', '4',
            '--certfile', os.path.join(certs_dir, 'server.pem'),
            '--keyfile', os.path.join(certs_dir, 'server.key'),
            '--reload', '--log-level', 'debug'
        ])

        # Encerrar instâncias existentes do Celery
        self.stdout.write("Killing existing Celery processes...")
        subprocess.run(['pkill', '-9', '-f', 'celery -A core worker'])

        # Iniciar Celery
        self.stdout.write("Starting Celery...")
        subprocess.Popen([
            celery_path, '-A', 'core', 'worker', '--loglevel=info'
        ])
