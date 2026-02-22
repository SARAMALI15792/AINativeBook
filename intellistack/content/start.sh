#!/bin/sh
# Start script for content service
# Railway sets PORT dynamically, fallback to 3000 for local dev

PORT=${PORT:-3000}
echo "Starting serve on port $PORT"
exec serve build -s -p "$PORT"
