"""API Gateway Service Entry Point.

Single entry point for all user API requests to the IaaS Platform.
Handles authentication, authorization, request routing, and rate limiting.

Hybrid Architecture: Uses existing tools (Crossplane, NATS, etc.) for
commodity functionality, custom logic only where necessary.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application
app = FastAPI(
    title="IaaS Platform API Gateway",
    description="Single entry point for all IaaS Platform API requests",
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
    """Health check endpoint for API Gateway."""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "architecture": "hybrid",
        "uses": ["crossplane", "nats", "postgresql", "redis", "minio"],
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "IaaS Platform API Gateway",
        "version": "0.1.0",
        "architecture": "hybrid",
        "docs": "/api/docs",
    }


# TODO: Add routers
# from src.api_gateway.routers import vms, storage, network, auth
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
# app.include_router(vms.router, prefix="/api/v1/vms", tags=["compute"])
# app.include_router(storage.router, prefix="/api/v1/storage", tags=["storage"])
# app.include_router(network.router, prefix="/api/v1/network", tags=["network"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api_gateway.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
    )
