# smart_secure/management/commands/django_stop.py

from django.core.management.base import BaseCommand
import subprocess
import os
import signal

class Command(BaseCommand):
    help = 'Stop the Django project services'

    def handle(self, *args, **options):
        # Encerrar Gunicorn usando a porta 8000 (ajuste conforme necessário)
        self.terminate_by_port(8000, "Gunicorn")

        # Encerrar processos do Celery
        self.terminate_celery_processes()

    def terminate_by_port(self, port, process_name):
        self.stdout.write(f"Terminating {process_name} processes using port {port}...")
        try:
            for pid in self.get_pids_by_port(port):
                self.terminate_process(pid)
        except Exception as e:
            self.stderr.write(str(e))

    def get_pids_by_port(self, port):
        pids = set()
        try:
            output = subprocess.check_output(['lsof', '-ti', f':{port}']).decode().strip()
            for pid in output.split('\n'):
                pids.add(int(pid))
        except subprocess.CalledProcessError:
            # No process found listening on the port
            pass
        return pids


    def terminate_process(self, pid):
        if self.is_process_running(pid):
            os.kill(pid, signal.SIGTERM)
            self.stdout.write(f"Sent SIGTERM to process {pid}")
            subprocess.run(['sleep', '5'])
            if self.is_process_running(pid):
                os.kill(pid, signal.SIGKILL)
                self.stdout.write(f"Sent SIGKILL to process {pid}")

    def is_process_running(self, pid):
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    def terminate_celery_processes(self):
        self.stdout.write("Terminating Celery processes...")
        try:
            subprocess.run(['pkill', '-15', '-f', 'celery -A core worker'])
            subprocess.run(['sleep', '5'])
            subprocess.run(['pkill', '-9', '-f', 'celery -A core worker'])
        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Failed to terminate Celery processes: {e}")
