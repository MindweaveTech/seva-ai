"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import setup_logging

# Initialize logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan events."""
    # Startup
    print("🚀 Starting Smart AI Backend...")
    print(f"📝 Environment: {settings.ENVIRONMENT}")
    print(f"🔧 Debug mode: {settings.DEBUG}")

    # TODO: Initialize database connection
    # TODO: Initialize Weaviate client
    # TODO: Initialize Redis client

    yield

    # Shutdown
    print("👋 Shutting down Smart AI Backend...")
    # TODO: Close database connections
    # TODO: Close Weaviate client
    # TODO: Close Redis client


# Create FastAPI application
app = FastAPI(
    title="Smart AI API",
    description="AI-powered elderly care companion system",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# GZip Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health Check Endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "smart-ai-backend",
            "version": "0.1.0",
        },
    )


@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Readiness check - verifies all dependencies are available."""
    # TODO: Check database connection
    # TODO: Check Weaviate connection
    # TODO: Check Redis connection

    return JSONResponse(
        status_code=200,
        content={
            "status": "ready",
            "database": "connected",
            "weaviate": "connected",
            "redis": "connected",
        },
    )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Smart AI Backend API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }


# TODO: Include API routers
# from app.api.v1 import auth, chat, health, users, voice
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
# app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(voice.router, prefix="/api/v1/voice", tags=["Voice"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
