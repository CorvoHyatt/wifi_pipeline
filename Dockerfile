# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app

EXPOSE 8000

# Ejecutar el script de inicialización antes de levantar la API
CMD ["bash", "-c", "python app/init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]