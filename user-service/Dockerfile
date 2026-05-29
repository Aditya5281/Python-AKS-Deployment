# ── Stage 1: Builder ──────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies into a temp folder (clean layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Final Image ──────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy only installed packages from builder (no pip cache)
COPY --from=builder /install /usr/local

# Copy app code
COPY app.py .

# Security: non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

EXPOSE 5001

# Gunicorn: production WSGI server
# 2 workers per container, timeout 120s
CMD ["gunicorn", "--bind", "0.0.0.0:5001", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:app"]