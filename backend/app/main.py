"""
Main FastAPI application
Budget Import/Export with AI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from .routes import convert_router, ai_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Budget Import/Export API",
    description="API for converting and processing budget files (BC3, PDF) with AI enhancement",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Budget Import/Export API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    ai_enabled = bool(os.getenv('ANTHROPIC_API_KEY'))

    return {
        "status": "healthy",
        "ai_enabled": ai_enabled,
        "features": {
            "bc3_parser": True,
            "bc3_generator": True,
            "pdf_generator": True,
            "pdf_extractor": ai_enabled,
            "ai_enhancement": ai_enabled
        }
    }


# Include routers
app.include_router(convert_router)
app.include_router(ai_router)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("API_PORT", 8000))
    host = os.getenv("API_HOST", "0.0.0.0")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True
    )
