#!/bin/bash

# Definir variáveis para o clone
GIT_REPO="https://github.com/cosmeaf/django_smartmecanico_006.git"
CLONE_DIR="/var/www/django_smartmecanico_006"
TARGET_DIR="/var/www/smartmecanico"

# Clonar o repositório Git
git clone "$GIT_REPO" "$CLONE_DIR"

# Mover o diretório clonado para o nome alvo
mv "$CLONE_DIR" "$TARGET_DIR"


# Definir variáveis para o usuário
USERNAME="developer"
PASSWORD="Smart@2023Smart@2023"
COMMENT="Smart Mecânico User Administrator"

# Criar o usuário 'developer'
useradd --create-home --home-dir "$TARGET_DIR" --shell /bin/bash --comment "$COMMENT" "$USERNAME"

# Definir a senha para o usuário 'developer'
echo "$USERNAME:$PASSWORD" | chpasswd

# Atualizar o usuário com o diretório correto e as permissões
usermod --home "$TARGET_DIR" --move-home --shell /bin/bash --comment "$COMMENT" "$USERNAME"

# Mudar a propriedade do diretório para o usuário 'developer'
chown -R "$USERNAME":"$USERNAME" "$TARGET_DIR"


# Instalar dependências globais
apt update && apt upgrade -y
apt install -y mysql-client-core-8.0 software-properties-common python3 python3.10-venv libmysqlclient-dev python3-dev default-libmysqlclient-dev build-essential

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

# Mudar a propriedade do diretório para o usuário 'developer'
chown -R "$USERNAME":"$USERNAME" "$TARGET_DIR"

# Ajustar as permissões do arquivo .env
chown "$USERNAME":"$USERNAME" "$TARGET_DIR/.env"
chmod 600 "$TARGET_DIR/.env"
