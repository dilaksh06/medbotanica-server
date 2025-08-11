# Put your model load/predict logic here.
# For now a dummy async function that returns a mock result.

async def load_model():
    # load transformer model / weights
    return None

async def predict_image(image_path: str) -> dict:
    # Replace with actual inference call when model ready.
    # Example returned shape:
    return {
        "predictions": [
            {"label": "Ocimum tenuiflorum (Tulsi)", "confidence": 0.89},
            {"label": "Ocimum basilicum (Basil)", "confidence": 0.07}
        ],
        "caption": "A small green herb, looks like tulsi"
    }
