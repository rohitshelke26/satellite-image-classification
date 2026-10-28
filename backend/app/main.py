from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import ALLOWED_ORIGINS
from app.api.routes import classes, health, prediction
from app.model_loader import ModelLoader
from app import model_loader

app = FastAPI(title="TerraVision AI API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(classes.router, prefix="/api")
app.include_router(prediction.router, prefix="/api")


@app.get("/api", include_in_schema=False)
@app.get("/api/", include_in_schema=False)
def api_root():
    return {
        "name": "TerraVision AI API",
        "docs": "/docs",
        "health": "/api/health",
        "classes": "/api/classes",
        "predict": "/api/predict",
    }

FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if FRONTEND_DIST.is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def frontend(full_path: str):
        if full_path == "api" or full_path.startswith("api/"):
            return JSONResponse(
                status_code=404,
                content={"detail": "API route not found. See /docs for available endpoints."},
            )
        requested_file = FRONTEND_DIST / full_path
        if full_path and requested_file.is_file():
            return FileResponse(requested_file)
        return FileResponse(FRONTEND_DIST / "index.html")


@app.on_event("startup")
def warm_model():
    from app.config import MODEL_PATH

    model_loader.loader = ModelLoader(MODEL_PATH)
