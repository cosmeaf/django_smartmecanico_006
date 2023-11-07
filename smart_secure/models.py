from django.db import models
from dashboard.models.user_model import CustomUser
from dashboard.models.base_model import Base
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import shutil
import subprocess

# Define a localização onde os certificados serão armazenados
certificate_storage = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'certs'))

class SSLCertificate(Base):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='certificate')
    name = models.CharField('Desciçao para SSL', max_length=100)
    # Usamos um campo FileField mas não armazenamos o arquivo diretamente
    certificate = models.FileField(storage=certificate_storage, upload_to='tmp/')
    private_key = models.FileField(storage=certificate_storage, upload_to='tmp/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Caminhos padrão onde o Gunicorn espera encontrar os certificados
        cert_path = os.path.join(settings.MEDIA_ROOT, 'certs', 'server.pem')
        key_path = os.path.join(settings.MEDIA_ROOT, 'certs', 'server.key')

        # Renomear os arquivos carregados para os nomes padrão
        if self.certificate:
            shutil.move(self.certificate.path, cert_path)
        if self.private_key:
            shutil.move(self.private_key.path, key_path)

        # Mudar o proprietário dos arquivos para o usuário 'developer'
        subprocess.run(['sudo', 'chown', 'developer:developer', cert_path])
        subprocess.run(['sudo', 'chown', 'developer:developer', key_path])

        # Mudar as permissões dos arquivos para que apenas o proprietário possa lê-los
        os.chmod(cert_path, 0o640)
        os.chmod(key_path, 0o640)
