from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from backend.routes.dashboard import router as dashboard_router
from backend.routes.eda import router as eda_router
from backend.routes.causal import router as causal_router
from backend.routes.simulation import router as simulation_router
from backend.routes.recommendations import router as recommendations_router
from backend.routes.products import router as products_router
from backend.routes.dataset import router as dataset_router

app = FastAPI(
    title="EconoCausal API",
    description="AI-Integrated Retail Pricing & Causal Decision Support System",
    version="1.0.0"
)

# Enable CORS for local dev servers and browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all route modules
app.include_router(dashboard_router)
app.include_router(eda_router)
app.include_router(causal_router)
app.include_router(simulation_router)
app.include_router(recommendations_router)
app.include_router(products_router)
app.include_router(dataset_router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EconoCausal Causal Inference & Pricing Engine",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
