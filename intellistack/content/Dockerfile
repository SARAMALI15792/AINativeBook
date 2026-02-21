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

# Create non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

# Copy built site from builder
COPY --from=builder /app/build ./build

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:${PORT:-3000}/ || exit 1

# Serve uses PORT env var automatically
CMD ["serve", "build", "-s"]

EXPOSE 3000
