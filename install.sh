#!/bin/bash

# Definir variáveis
PROJECT_DIR="/var/www/smartmecanico"
USERNAME="developer"
PASSWORD="Smart@2023Smart@2023"
GIT_REPO="https://github.com/cosmeaf/django_smartmecanico_006.git"

# Atualizar os pacotes do sistema
apt update && apt upgrade -y

# Instalar pacotes necessários
apt install mysql-client-core-8.0 software-properties-common python3 python3.10-venv libmysqlclient-dev python3-dev default-libmysqlclient-dev build-essential -y

# Definir variáveis de ambiente para compilação do cliente MySQL
export MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
export MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"

# Criar o usuário 'developer' com PROJECT_DIR como diretório home
if ! id "$USERNAME" &>/dev/null; then
    useradd --create-home --home-dir "$PROJECT_DIR" --shell /bin/bash "$USERNAME"
    echo "Senha do usuário $USERNAME definida."
    echo "$USERNAME:$PASSWORD" | chpasswd
else
    echo "Usuário $USERNAME já existe. Continuando com a instalação."
fi

# Mudar a propriedade do diretório
chown -R "$USERNAME":"$USERNAME" "$PROJECT_DIR"
chmod -R 755 "$PROJECT_DIR"

# Clonar o repositório Git dentro do diretório do projeto
if sudo -u "$USERNAME" -H git clone "$GIT_REPO" "$PROJECT_DIR"; then
    echo "Repositório clonado com sucesso."
else
    echo "Falha ao clonar o repositório. Verifique sua conexão de rede ou permissões."
    exit 1
fi

# Criar diretórios static e media
mkdir -p "$PROJECT_DIR/static"
mkdir -p "$PROJECT_DIR/media"
chown -R "$USERNAME":"$USERNAME" "$PROJECT_DIR"

# Configurar o ambiente virtual e instalar as dependências do Django
sudo -u "$USERNAME" -i <<EOF
cd "$PROJECT_DIR"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
# Adicionar aqui a instalação das dependências do Django, se necessário
# pip install -r requirements.txt

EOF

echo "Instalação concluída com sucesso."
