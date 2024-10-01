#!/bin/bash

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set up Django
echo "Setting up Django database..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# Start the server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
