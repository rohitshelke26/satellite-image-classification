from datetime import datetime, timezone

import numpy as np

from app.config import CLASSES
from app.model_loader import loader
from app.utils.preprocessing import preprocess_image


class InferenceService:
    def predict(self, content: bytes):
        tensor, dimensions = preprocess_image(content)
        model, error = loader.load()
        if error or model is None:
            raise RuntimeError(error or "The model is unavailable.")

        output = np.asarray(model.predict(tensor, verbose=0))
        if output.ndim != 2 or output.shape[0] != 1 or output.shape[1] != len(CLASSES):
            raise RuntimeError(
                f"Unexpected model output shape {output.shape}; expected (1, {len(CLASSES)})."
            )

        scores = np.asarray(output[0], dtype=float)
        if not np.all(np.isfinite(scores)):
            raise RuntimeError("The model returned non-finite scores.")
        best_index = int(np.argmax(scores))
        return {
            "predicted_class": CLASSES[best_index],
            "predicted_display_name": CLASSES[best_index].replace(
                "HerbaceousVegetation", "Herbaceous Vegetation"
            ).replace("AnnualCrop", "Annual Crop").replace("PermanentCrop", "Permanent Crop")
            .replace("SeaLake", "Sea / Lake"),
            "score": float(scores[best_index]),
            "scores": {
                CLASSES[index]: float(score)
                for index, score in enumerate(scores)
            },
            "image": {"width": dimensions[0], "height": dimensions[1]},
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_info": {
                "format": "Keras .keras",
                "input": "64 x 64 RGB",
                "output": "10-class softmax scores",
                "preprocessing": "Resize to 64 x 64, RGB, divide pixel values by 255",
            },
        }
