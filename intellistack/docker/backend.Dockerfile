# IntelliStack Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (as root)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Install Python dependencies (as root to ensure they install globally)
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (as root)
COPY backend/src ./src
COPY backend/alembic ./alembic
COPY backend/alembic.ini ./

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
