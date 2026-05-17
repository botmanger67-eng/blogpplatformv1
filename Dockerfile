FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (e.g., for database drivers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set environment variables
ENV FLASK_APP=app/__init__.py
ENV FLASK_ENV=production

# Expose port (Flask default)
EXPOSE 5000

# Run with gunicorn (production WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]