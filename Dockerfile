FROM python:3.12-slim AS base

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

FROM base AS dev

EXPOSE 8000

# Expose the port that the application listens on & run the application.
EXPOSE 8000
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS prod
# Copy the entrypoint script
COPY entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Run collectstatic with dummy build-time secrets
# These variables are only used during the build process and are not used in production
RUN SECRET_KEY="dummy-key-for-build" DATABASE_URL="sqlite:////tmp/db.sqlite3" python manage.py collectstatic --no-input

EXPOSE 10000

# The production command to start the server
CMD ["/app/entrypoint.sh"]
