FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

COPY requirements.txt .

# Instala apenas o necessário
RUN apt-get update && apt-get install -y gcc g++ \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc g++ && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
