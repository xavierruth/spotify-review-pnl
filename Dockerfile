# Stage 1: Builder - instala as dependências e ferramentas necessárias para build
FROM python:3.11-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copia requirements para cachear dependências
COPY requirements.txt .

# Instala ferramentas para build e as dependências Python
RUN apt-get update && apt-get install -y build-essential \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia o código fonte (se necessário no build)
COPY . .

# Stage 2: Final - imagem só com runtime, sem build tools e sem cache
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copia os pacotes Python instalados do builder para o local correto
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia seu código fonte
COPY --from=builder /app /app

EXPOSE 7860

CMD ["python", "app.py"]
