FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Só copia o requirements primeiro para aproveitar cache
COPY requirements.txt .

# Instala dependências do sistema (caso realmente precise)
RUN apt-get update && apt-get install -y build-essential \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia o resto do código
COPY . .

EXPOSE 7860

CMD ["python", "app.py"]