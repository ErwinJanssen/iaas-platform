"""Control Plane Service Entry Point.

This is the main entry point for the Control Plane service.
It initializes the FastAPI application and sets up the core business logic.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application
app = FastAPI(
    title="IaaS Platform Control Plane",
    description="Core business logic and orchestration service",
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
    """Health check endpoint for Control Plane."""
    return {"status": "healthy", "service": "control-plane"}


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning service information."""
    return {
        "name": "IaaS Platform Control Plane",
        "version": "0.1.0",
        "docs": "/api/docs",
    }


# TODO: Import and mount routers
# from src.control_plane.routers import resources, orchestration
# app.include_router(resources.router, prefix="/api/v1/resources", tags=["resources"])
# app.include_router(orchestration.router, prefix="/api/v1/orchestration", tags=["orchestration"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.control_plane.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="debug",
    )
