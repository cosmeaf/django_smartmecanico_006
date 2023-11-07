#!/bin/bash

# Função para encerrar processos por porta
terminate_by_port() {
    local port="$1"
    local process_name="$2"
    local processes=$(lsof -i :"$port" | awk '{if (NR!=1) {print $2}}')

    if [ -n "$processes" ]; then
        echo "Terminating $process_name processes using port $port..."
        for pid in $processes; do
            if kill -0 "$pid" 2>/dev/null; then  # Verifica se o processo ainda está ativo
                kill -15 "$pid"  # SIGTERM, pedir ao processo para fechar
                sleep 5  # Espera um pouco para ver se o processo termina
                if kill -0 "$pid" 2>/dev/null; then  # Checa novamente se o processo ainda está rodando
                    echo "Process $pid did not terminate, using SIGKILL."
                    kill -9 "$pid"  # SIGKILL, força o encerramento do processo
                fi
            else
                echo "Process $pid already terminated."
            fi
        done
    else
        echo "No $process_name processes found using port $port."
    fi
}

# Encerrar Gunicorn usando a porta 8000 (ajuste conforme necessário)
terminate_by_port 8000 "Gunicorn"

# Encerrar processos do Celery (substitua com o seu comando Celery)
echo "Terminating Celery processes..."
pkill -15 -f "celery -A smartmecanico worker"
sleep 5  # Espera e verifica novamente
pkill -9 -f "celery -A smartmecanico worker"
ps -ef|grep celery | grep celery | awk '{print $2}' | xargs kill -9

echo "Stop script completed."
