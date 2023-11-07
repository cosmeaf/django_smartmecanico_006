Instruções para Executar o Script:

Salve este conteúdo em um arquivo chamado install.sh.
Dê permissões de execução ao script com o comando chmod +x install.sh.
Execute o script como superusuário: sudo ./install.sh.
Notas Importantes:

Este script agora instala todos os pacotes adicionais que você mencionou.
As variáveis de ambiente MYSQLCLIENT_CFLAGS e MYSQLCLIENT_LDFLAGS são exportadas no script. Se precisarem ser persistentes, você pode querer adicioná-las ao arquivo ~/.bashrc ou /etc/environment.
O script assume que o nome do repositório é o mesmo que o nome do diretório do projeto e que o repositório será clonado diretamente para /var/www/smartmecanico. Se o repositório Git contiver um subdiretório com o código fonte, você precisará ajustar o caminho no script.
O script ativa o ambiente virtual e atualiza o pip, mas você precisará adicionar manualmente a linha para instalar as dependências do Django do arquivo requirements.txt se houver um.
O script não inclui a configuração de um servidor web ou um gateway de aplicativo WSGI como Gunicorn ou uWSGI. Isso precisará ser configurado separadamente.