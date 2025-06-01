FROM pytorch/pytorch:2.0.1-cpu-py3.10

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Copia e instala apenas as libs que não são torch (já vem instalada)
COPY requirements.txt .

# Remove torch do requirements para evitar duplicidade
RUN pip install --upgrade pip && \
    sed '/^torch==/d' requirements.txt > temp.txt && \
    pip install --no-cache-dir -r temp.txt && \
    rm temp.txt

# Copia seu código
COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
