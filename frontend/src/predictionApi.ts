export interface PredictionResult {
  predicted_class: string;
  predicted_display_name: string;
  score: number;
  scores: Record<string, number>;
  image: { width: number; height: number };
  timestamp: string;
  model_info: Record<string, string>;
}

const API = import.meta.env.VITE_API_BASE_URL || "/api";

export async function predictImage(file: File): Promise<PredictionResult> {
  const form = new FormData();
  form.append("file", file);
  let response: Response;
  try {
    response = await fetch(`${API}/predict`, { method: "POST", body: form });
  } catch {
    throw new Error("Cannot reach the TerraVision API. Confirm that the backend is running.");
  }
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.detail || "The image could not be classified.");
  }
  return body;
}
