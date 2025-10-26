import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os
# ✅ Hugging Face public model ID
MODEL_ID = "dilaksh06/medbotanica"

# --- Load model once (global) to avoid reloading on each request ---
print(f"🔄 Loading BLIP model from Hugging Face repo {MODEL_ID} ...")
try:
    processor = BlipProcessor.from_pretrained(MODEL_ID)
    model = BlipForConditionalGeneration.from_pretrained(MODEL_ID)

    # Optional: use GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()

    print(f"✅ Model successfully loaded on {device}")
except Exception as e:
    print(f"❌ Failed to load model: {e}")
    processor, model, device = None, None, "cpu"


# === Caption Generation Function ===
def generate_caption_from_path(image_path: str) -> str:
    """
    Generates an image caption using the fine-tuned BLIP model.

    Args:
        image_path (str): Local path to the image file.

    Returns:
        str: The generated caption or an error message.
    """
    if not os.path.exists(image_path):
        return f"Error: Image not found at {image_path}"

    if processor is None or model is None:
        return "Error: Model not loaded properly. Check server logs."

    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(image, return_tensors="pt").to(device)

        # Generate caption (customize parameters as needed)
        output_ids = model.generate(**inputs, max_length=50, num_beams=3)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)

        print(f"🧠 Caption generated: {caption}")
        return caption

    except Exception as e:
        print(f"❌ Caption generation failed: {e}")
        return f"Caption generation failed: {e}"
