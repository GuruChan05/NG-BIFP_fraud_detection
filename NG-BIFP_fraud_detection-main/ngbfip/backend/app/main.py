from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1 import api_router
from app.db.base import engine, Base
import logging

# Create tables
Base.metadata.create_all(bind=engine)

# Logging (must be configured before seed so logger is available)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Seed demo data on first startup
try:
    from app.db.seed import seed_if_empty
    seed_if_empty()
except Exception as _seed_err:
    logger.warning("Seeding skipped: %s", _seed_err)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="NG-BIFP Fraud Detection System API"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to NG-BIFP Fraud Detection System",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
