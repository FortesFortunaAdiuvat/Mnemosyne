from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI instance
app = FastAPI(
    title="Mnemosyne API",
    description="A spaced repetition learning system API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello_world():
    """Hello World endpoint"""
    return {"message": "Hello World from Mnemosyne API!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mnemosyne-api"}

@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Mnemosyne API",
        "version": "1.0.0",
        "description": "A spaced repetition learning system",
        "endpoints": {
            "root": "/",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }
