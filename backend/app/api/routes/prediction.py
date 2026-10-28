import asyncio

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import MAX_UPLOAD_BYTES
from app.services.inference_service import InferenceService

router = APIRouter()
service = InferenceService()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    content_type = file.content_type or ""
    if content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=415, detail="Only JPG and PNG images are supported.")

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="The uploaded image is too large.")
    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    try:
        return await asyncio.wait_for(asyncio.to_thread(service.predict, content), timeout=20)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except asyncio.TimeoutError as exc:
        raise HTTPException(status_code=504, detail="Inference timed out.") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
