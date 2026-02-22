# Docusaurus Content Site Dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including devDependencies for build)
RUN npm ci

# Copy source files
COPY . .

# Build static site
RUN npm run build

# Runtime stage
FROM node:20-alpine

WORKDIR /app

# Install serve globally
RUN npm install -g serve@14

# Create non-root user (use existing node user or create new one)
RUN if ! getent group appuser > /dev/null 2>&1; then \
        addgroup -g 1001 appuser; \
    fi && \
    if ! id -u appuser > /dev/null 2>&1; then \
        adduser -D -u 1001 -G appuser appuser; \
    fi && \
    chown -R appuser:appuser /app

# Copy built site from builder
COPY --from=builder /app/build ./build

# Copy start script
COPY start.sh ./
RUN chmod +x start.sh

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:${PORT:-3000}/ || exit 1

# Start the server using the wrapper script
CMD ["./start.sh"]

EXPOSE 3000
