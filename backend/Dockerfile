FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install Chrome and ChromeDriver for Selenium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements/ ./requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt

# Copy project
COPY . .

EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000
