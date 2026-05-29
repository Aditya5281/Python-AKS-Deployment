# Use slim Python image (smaller, production-safe)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies first (layer caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create a non-root user (industry security standard)
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expose port
EXPOSE 5001

# Run with gunicorn (production WSGI server, NOT flask dev server)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "--timeout", "60", "app:app"]