# smart_secure/management/commands/ssl_generate.py

import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import CommandError

class Command(BaseCommand):
    help = 'Generate a self-signed SSL certificate'

    def add_arguments(self, parser):
        # Adiciona uma flag que pode ser usada para forçar a recriação dos certificados
        parser.add_argument('--force', action='store_true', help='Force the regeneration of SSL certificates')
        parser.add_argument('--web', action='store_true', help='Run without interactive input (for web usage)')

    def handle(self, *args, **options):
        certs_dir = os.path.join(settings.BASE_DIR, 'smart_secure', 'certs')

        # Verifica se o diretório certs existe
        if os.path.exists(certs_dir):
            if options['web'] or options['force']:
                subprocess.run(['rm', '-rf', certs_dir])
                os.makedirs(certs_dir)
            else:
                self.stdout.write(self.style.WARNING('O diretório de certificados já existe.'))
                overwrite = input('Deseja recriar os certificados? (s/N): ')
                if overwrite.lower() != 's':
                    self.stdout.write(self.style.NOTICE('Operação cancelada.'))
                    return

        else:
            os.makedirs(certs_dir)

        try:
            # Gere o certificado autoassinado e a chave privada
            subprocess.run([
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-nodes',
                '-out', os.path.join(certs_dir, 'server.crt'),
                '-keyout', os.path.join(certs_dir, 'server.key'),
                '-days', '365',
                '-subj', '/C=BR/ST=Rio de Janeiro/L=Rio de Janeiro/O=Smart Secure/OU=IT/CN=smartsecure.app/emailAddress=cosmeaf@gmail.com'
            ], check=True)

            # Combine server.crt e server.key para criar um arquivo .pem
            with open(os.path.join(certs_dir, 'server.pem'), 'wb') as pem_file:
                with open(os.path.join(certs_dir, 'server.crt'), 'rb') as crt_file:
                    pem_file.write(crt_file.read())
                with open(os.path.join(certs_dir, 'server.key'), 'rb') as key_file:
                    pem_file.write(key_file.read())

            self.stdout.write(self.style.SUCCESS('Os arquivos server.crt, server.key e server.pem foram criados no diretório certs.'))

        except subprocess.CalledProcessError as e:
            raise CommandError(self.style.ERROR(f"Erro ao gerar os certificados: {e}"))
