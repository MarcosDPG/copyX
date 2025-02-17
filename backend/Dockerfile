FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
COPY backend/django.sh .
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY ../frontend /app/frontend
EXPOSE 8000
RUN chmod +x django.sh
CMD ["sh","./django.sh"]