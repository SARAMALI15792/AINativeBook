"""
Vercel serverless function handler for FastAPI backend.
This file adapts the FastAPI app to work with Vercel's serverless functions.
"""

from mangum import Mangum
from src.main import app

# Mangum adapter converts ASGI app (FastAPI) to AWS Lambda/Vercel handler
handler = Mangum(app, lifespan="off")
