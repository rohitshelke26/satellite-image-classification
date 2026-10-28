from fastapi import APIRouter

from app.model_loader import loader

router = APIRouter()


@router.get("/health")
def health():
    model, error = loader.load()
    return {
        "status": "ok",
        "model_loaded": model is not None and error is None,
    }
