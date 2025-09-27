#!/bin/sh

# Exit on error
set -o errexit

# Run database migrations
python manage.py migrate

# Start the Gunicorn server
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000
