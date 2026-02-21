# IntelliStack Backend Dockerfile
# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (avoid UID/GID conflicts)
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check (longer start-period for migrations)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run migrations then start application
CMD sh -c "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"
