#!/bin/sh
# Start script for content service
# Use PORT if set by Railway, otherwise default to 3000

if [ -z "$PORT" ]; then
  echo "PORT not set, using default 3000"
  PORT=3000
else
  echo "Starting serve on port $PORT"
fi

exec serve build -s -p "$PORT"
