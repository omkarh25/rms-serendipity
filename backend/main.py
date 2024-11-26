"""
Main FastAPI application module for RMS (Rating Management System).

This module initializes the FastAPI application, sets up middleware,
configures logging, and includes all API routers.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
import logging
import time
from typing import Callable
from datetime import datetime

from config import get_settings, init_logging
from database import init_db
from routers import projects_router, ratings_router, users_router

# Initialize logging
init_logging()
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="RMS API",
    description="""
    Rating Management System API for Dhoom Studios.
    
    Features:
    - Project management
    - Rating system based on Navarasa
    - Content analysis with philosophical perspectives
    """,
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None  # Disable default redoc
)

# Get settings
settings = get_settings()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    """Log all HTTP requests with timing information."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.2f}s"
    )
    
    return response

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for logging errors."""
    logger.error(f"Global error occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Custom API documentation
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Serve custom Swagger UI documentation."""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="RMS API Documentation",
        swagger_favicon_url="/static/favicon.ico"
    )

# Include routers
app.include_router(projects_router, prefix="/api/v1")
app.include_router(ratings_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Execute actions on application startup."""
    logger.info("Starting up RMS API")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Execute actions on application shutdown."""
    logger.info("Shutting down RMS API")

@app.get("/")
async def root():
    """Root endpoint to verify API status."""
    logger.info("Root endpoint accessed")
    return {
        "status": "active",
        "message": "Welcome to RMS API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    logger.info("Health check endpoint accessed")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "api": "up",
            "database": "up"  # This will be implemented with actual DB health check
        }
    }

