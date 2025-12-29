FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

# Копируем .env, если нужно (можно монтировать volume при запуске)
# COPY .env /app/.env

CMD ["python", "-m", "app.main"]
