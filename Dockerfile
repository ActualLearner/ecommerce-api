FROM python:3.12-slim

# set workdir
WORKDIR /app

# Install only needed system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
  libpq5 \
  && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY ./src/ .

# Run collectstatic with dummy build-time secrets
# These variables are only used during the build process and are not used in production
RUN SECRET_KEY="dummy-key-for-build" DATABASE_URL="sqlite:////tmp/db.sqlite3" python manage.py collectstatic --no-input

EXPOSE 10000

# The production command to start the server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:10000"]
