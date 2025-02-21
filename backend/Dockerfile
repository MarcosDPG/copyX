FROM python:3.9-slim

WORKDIR /app

# Copy the necessary files into the container
COPY backend/requirements.txt .
COPY backend/django.sh .
COPY backend/wait-for-it.sh .

# Install the necessary dependencies in the container
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install the necessary Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend files into the container
COPY ../frontend /app/frontend

# Assign the necessary permissions to the files
RUN chmod +x wait-for-it.sh
RUN chmod +x django.sh

# Expose the port 8000
EXPOSE 8000
