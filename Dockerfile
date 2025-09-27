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

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
