#!/bin/bash

# Definir variáveis para o clone
GIT_REPO="https://github.com/cosmeaf/django_smartmecanico_006.git"
CLONE_DIR="/var/www/django_smartmecanico_006"
TARGET_DIR="/var/www/smartmecanico"

# Cleaner process Django and Celery active on Server
bash /var/www/smartmecanico/setup/scripts/stop_django.sh

# Verificar e remover o diretório existente, se necessário
if [ -d "$CLONE_DIR" ]; then
    echo "Excluindo o diretório antigo: $CLONE_DIR"
    rm -rf "$CLONE_DIR"
fi

if [ -d "$TARGET_DIR" ]; then
    echo "Excluindo o diretório antigo: $TARGET_DIR"
    rm -rf "$TARGET_DIR"
fi

# Clonar o repositório Git
git clone "$GIT_REPO" "$CLONE_DIR"

# Mover o diretório clonado para o nome alvo
mv "$CLONE_DIR" "$TARGET_DIR"

# Definir variáveis para o usuário
USERNAME="developer"
PASSWORD="Smart@2023Smart@2023"
COMMENT="Smart Mecânico User Administrator"

# Criar o usuário 'developer', se ele não existir
if id "$USERNAME" &>/dev/null; then
    echo "Usuário $USERNAME já existe"
else
    echo "Criando usuário $USERNAME"
    sudo useradd --create-home --home-dir "$TARGET_DIR" --shell /bin/bash --comment "$COMMENT" "$USERNAME"
    echo "$USERNAME:$PASSWORD" | sudo chpasswd
fi

# Atualizar o usuário com o diretório correto e as permissões
sudo usermod --home "$TARGET_DIR" --move-home --shell /bin/bash --comment "$COMMENT" "$USERNAME"

# Mudar a propriedade do diretório para o usuário 'developer'
sudo chown -R "$USERNAME":"$USERNAME" "$TARGET_DIR"

# Instalar dependências globais (requer privilégios de superusuário)
# As dependências globais devem ser gerenciadas cuidadosamente. Considere usar um ambiente virtual.

# Ativar o ambiente virtual e instalar as dependências
cd "$TARGET_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Criar arquivos de configuração do projeto, como .env
cat > "$TARGET_DIR/.env" << EOF
# SECURITY DJANGO
SECRET_KEY='&fhxngtjm-m9(_gg-aqw$r29dfklb%pim60mc9fw!^9d#0odq='

# DEBUG SETTINGS: don't run with debug turned on in production!
DEBUG = True
# ALLOWED HOSTS AND URL
ALLOWED_HOSTS=['*','localhost','127.0.0.1', '0.0.0.0', 'smartmecanico.app', '85.31.231.240']

# GEO LOCATION API KEY
API_KEY='c8d0b8d0472849ec89f000bb2a97896f'

# SMTP SERVICE
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='cosmeaf@gmail.com'
EMAIL_HOST_PASSWORD='qpnmttbckwldynkf'
EMAIL_USE_TLS=true
EOF

# Ajustar as permissões do arquivo .env
sudo chown "$USERNAME":"$USERNAME" "$TARGET_DIR/.env"
sudo chmod 600 "$TARGET_DIR/.env"
