#!/bin/sh

# Exit on error
set -o errexit

# Run database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create the admin user (safe to run multiple times)
echo "Creating admin user..."
python manage.py createadmin

# Start the Gunicorn server
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000
