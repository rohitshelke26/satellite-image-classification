from fastapi import APIRouter

from app.config import CLASSES

router = APIRouter()


DISPLAY_NAMES = {
    "HerbaceousVegetation": "Herbaceous Vegetation",
    "AnnualCrop": "Annual Crop",
    "PermanentCrop": "Permanent Crop",
    "SeaLake": "Sea / Lake",
}


@router.get("/classes")
def get_classes():
    return [
        {"identifier": name, "display_name": DISPLAY_NAMES.get(name, name)}
        for name in CLASSES
    ]
