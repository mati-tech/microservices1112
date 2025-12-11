# FROM python:3.10
# WORKDIR /code

# RUN mkdir -p /app/storage/materials

# COPY ./requirements.txt /code/
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app

# EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]


FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PostgreSQL client
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 fastapi && chown -R fastapi:fastapi /app
USER fastapi

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]