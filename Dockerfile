FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Copia apenas o requirements para cachear dependências
COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia o restante do código
COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
