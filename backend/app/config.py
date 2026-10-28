import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = Path(os.getenv("MODEL_PATH", BASE_DIR / "model" / "satellite_cnn.keras"))
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", 10 * 1024 * 1024))
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

CLASSES = [
    "Forest",
    "HerbaceousVegetation",
    "SeaLake",
    "AnnualCrop",
    "Industrial",
    "Highway",
    "PermanentCrop",
    "River",
    "Residential",
    "Pasture",
]
