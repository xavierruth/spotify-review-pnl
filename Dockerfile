FROM pytorch/pytorch:2.0.1-cpu

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt .

# Instala somente o restante (torch já vem incluso na imagem)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
