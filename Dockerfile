# === Stage 1: Builder (deps + tests) ===
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запускаем тесты на этапе сборки
# RUN pytest --junitxml=/app/test-results/report.xml

# === Stage 2: Runtime (лёгкий образ) ===
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/app ./app

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.main

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]