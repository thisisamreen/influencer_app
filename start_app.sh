#!/bin/bash

# Start Redis server
echo "Starting Redis server..."
redis-server &

# Start MailHog
echo "Starting MailHog..."
mailhog &

# Start Celery worker
echo "Starting Celery worker..."
celery -A run.celery worker --loglevel=info &

# Start Celery beat
echo "Starting Celery beat..."
celery -A run.celery beat --loglevel=info &

# Start Flask app
echo "Starting Flask app..."
python run.py
