# Etapa 1: Build - instala dependências e pacotes necessários
FROM python:3.11-slim AS builder

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema necessárias para compilar pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia apenas o requirements.txt para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Etapa 2: Runtime - imagem final com apenas o necessário para executar a aplicação
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copia as dependências Python instaladas na etapa de build
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia o código da aplicação
COPY --from=builder /app /app

EXPOSE 7860

CMD ["python", "app.py"]
