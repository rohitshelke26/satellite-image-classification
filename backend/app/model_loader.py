import threading
from pathlib import Path


class ModelLoader:
    def __init__(self, model_path: Path):
        self.model_path = model_path
        self.model = None
        self.error = None
        self._lock = threading.Lock()

    def load(self):
        if self.model is not None or self.error is not None:
            return self.model, self.error
        with self._lock:
            if self.model is not None or self.error is not None:
                return self.model, self.error
            try:
                import keras

                self.model = keras.models.load_model(self.model_path, compile=False)
            except Exception as exc:
                self.error = f"{type(exc).__name__}: {exc}"
        return self.model, self.error


from app.config import MODEL_PATH

loader = ModelLoader(MODEL_PATH)
