# Project setup

## Structure

```text
sat/
├── backend/app/
│   ├── api/routes/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   ├── main.py
│   └── model_loader.py
├── frontend/src/
├── model/satellite_cnn.keras
├── satellite_cnn.keras
└── docs/
```

## Prerequisites

- Python 3.11
- Node.js 20 or newer
- The TensorFlow/Keras model dependencies listed in `backend/requirements.txt`

## Environment

Backend variables:

- `MODEL_PATH`: Keras model path; default is `../model/satellite_cnn.keras`
- `MAX_UPLOAD_BYTES`: upload limit; default 10 MB
- `CORS_ORIGINS`: comma-separated frontend origins; default is `http://localhost:5173`

Frontend variables:

- `VITE_API_BASE_URL`: API prefix; default is `http://localhost:8000/api`

Copy the supplied `.env.example` files when custom configuration is needed.

## API

- `GET /api/health`
- `GET /api/classes`
- `POST /api/predict` with multipart field `file`

The prediction endpoint accepts JPEG and PNG images, validates decoding, converts them to RGB, resizes to 64 × 64, normalizes values, and runs the Keras model.

## Render deployment

The repository includes `render.yaml`. It creates one Python web service that:

1. Builds the React application.
2. Installs TensorFlow/Keras and the FastAPI dependencies.
3. Starts Uvicorn on Render's assigned `$PORT`.
4. Serves the React production bundle and `/api/*` routes from the same origin.

Use Python 3.11. The blueprint expects the model at `model/satellite_cnn.keras`. Do not rename, omit, or upload a replacement without updating `MODEL_PATH`.
