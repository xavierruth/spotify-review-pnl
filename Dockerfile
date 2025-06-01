FROM python:3.11.9-slim-bookworm

# Evita mensagens interativas durante instalação
ENV DEBIAN_FRONTEND=noninteractive

# Diretório de trabalho
WORKDIR /app

# Copia tudo para o container
COPY . .

# Instala dependências do sistema e Python
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Expõe a porta padrão do Spaces
EXPOSE 7860

# Comando para rodar o app
CMD ["python", "app.py"]
