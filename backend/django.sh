#!/bin/bash
echo "Deleting old migrations..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
echo ====================================
echo "Creating Migrations..."
python manage.py makemigrations
echo ====================================
echo "Starting Migrations..."
python manage.py migrate
echo ====================================
echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000