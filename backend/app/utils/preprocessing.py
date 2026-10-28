import io

import numpy as np
from PIL import Image, ImageOps


def preprocess_image(content: bytes, target_size=(64, 64)):
    try:
        image = Image.open(io.BytesIO(content))
        image.verify()
    except Exception as exc:
        raise ValueError("The uploaded file is not a valid image.") from exc

    image = Image.open(io.BytesIO(content))
    image = ImageOps.exif_transpose(image).convert("RGB")
    image = ImageOps.fit(image, target_size, method=Image.Resampling.BILINEAR)
    pixels = np.asarray(image, dtype=np.float32) / 255.0
    return np.expand_dims(pixels, axis=0), image.size
