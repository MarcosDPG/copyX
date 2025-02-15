FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY ../frontend /app/frontend
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]