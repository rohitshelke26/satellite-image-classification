# TerraVision AI

TerraVision AI is a full-stack satellite image land-cover classifier. It uses the existing trained Keras model to generate estimates for ten supported categories.

## Run locally

### Backend

Use Python 3.11 for this model:

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. API documentation is available at http://localhost:8000/docs.

## Deploy to Render

1. Push the project repository to GitHub.
2. In Render, choose **New > Blueprint** and select the repository.
3. Render uses `render.yaml` to create one web service containing both the React frontend and FastAPI API.
4. Change `CORS_ORIGINS` after the service receives its final URL if needed. The frontend and API are served from the same Render origin, so this value may remain on the generated hostname.
5. Confirm the web service has enough memory for TensorFlow/Keras. The starter plan is a starting point; use a larger instance if the model process is terminated for memory usage.

The production build is performed by Render, then FastAPI serves `frontend/dist`. Set `VITE_API_BASE_URL=/api` for a same-origin deployment.

## Model

The preserved model is at `model/satellite_cnn.keras`. It is also retained at the project root. The backend also accepts the original root location:

```text
MODEL_PATH=../model/satellite_cnn.keras
```

The Keras model has input shape `(64, 64, 3)` and produces ten scores. Images are converted to RGB, resized to 64 × 64, and normalized by 255. The final softmax layer supplies raw model scores.

## Supported identifiers

Forest, HerbaceousVegetation, SeaLake, AnnualCrop, Industrial, Highway, PermanentCrop, River, Residential, Pasture.

## Tests

```bash
cd backend
PYTHONPATH=. python3.11 -m pytest -q
cd ../frontend
npm run build
```

## Responsible use

Predictions are model-generated estimates, not verified ground truth or calibrated probability estimates. They should be validated with appropriate geospatial reference data.
