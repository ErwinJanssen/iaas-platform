"""Failover Manager Service Entry Point.

Automatic provider failover and health monitoring for the IaaS Platform.
Monitors provider health and triggers failover when outages are detected.

Hybrid Architecture: Our primary differentiator.
Uses Crossplane for resource recreation during failover.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application
app = FastAPI(
    title="IaaS Platform Failover Manager",
    description="Automatic provider failover and health monitoring service. Uses Crossplane for resource recreation.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Failover Manager."""
    return {
        "status": "healthy",
        "service": "failover-manager",
        "architecture": "hybrid",
        "uses": ["crossplane", "nats", "postgresql"],
        "primary_differentiator": True,
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning service information."""
    return {
        "name": "IaaS Platform Failover Manager",
        "version": "0.1.0",
        "architecture": "hybrid",
        "docs": "/api/docs",
        "unique_value": "automatic_multi_provider_failover",
    }


# TODO: Add routers
# from src.failover_manager.routers import health, failover
# app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
# app.include_router(failover.router, prefix="/api/v1/failover", tags=["failover"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.failover_manager.main:app",
        host="0.0.0.0",
        port=8002,
        reload=True,
        log_level="debug",
    )
