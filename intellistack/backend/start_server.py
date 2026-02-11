#!/usr/bin/env python3
"""Start IntelliStack backend server"""

import os
import sys
import uvicorn

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    print("="*60)
    print("IntelliStack Backend Server Starting")
    print("="*60)
    print()
    print("Loading configuration from .env...")
    print(f"Database URL: {os.getenv('DATABASE_URL', 'NOT SET')}")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"Debug: {os.getenv('DEBUG', 'false')}")
    print()
    print("Starting FastAPI server on http://127.0.0.1:8000...")
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("Health Check: http://127.0.0.1:8000/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("="*60)
    print()

    try:
        uvicorn.run(
            "src.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info",
        )
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
