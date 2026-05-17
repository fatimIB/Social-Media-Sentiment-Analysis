"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router

# Create FastAPI application
app = FastAPI(
    title="Sentiment Analysis API",
    description="API for Reddit sentiment analysis",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router)


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "Sentiment Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "available_endpoints": [
            "/analyze",
            "/health"
        ]
    }