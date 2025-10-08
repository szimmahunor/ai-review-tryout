from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.python_fastapi_project.api.product_api import router as product_router
from src.python_fastapi_project.api.cart_api import router as cart_router
from src.python_fastapi_project.repository.database import database_lifespan
from dotenv import load_dotenv
import os

# Load environment variables from .env file to os.getenv
load_dotenv("configs/.env")

# Create FastAPI application
app = FastAPI(
    title="Product Management API",
    description="A FastAPI application for managing products with CRUD operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=database_lifespan
)

# Add CORS middleware with secure configuration
origins = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(product_router, prefix="/api")
app.include_router(cart_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Product Management API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
