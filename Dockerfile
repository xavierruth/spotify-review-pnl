FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TRANSFORMERS_CACHE=/tmp/huggingface

WORKDIR /app

COPY requirements.txt .

# Instala dependências 
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc g++ \
    && pip install --upgrade pip \
    && pip install --no-cache-dir numpy==1.24.4 scikit-learn==1.3.2 \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc g++ build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

# Cria diretório de cache com permissão
RUN mkdir -p /tmp/huggingface && chmod -R 777 /tmp/huggingface

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
