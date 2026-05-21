import torch
import numpy as np
import cv2
from transformers import AutoImageProcessor, AutoModelForImageClassification

# -----------------------------
# Load model ONCE
# -----------------------------
processor = AutoImageProcessor.from_pretrained("umm-maybe/ai-image-detector")
model = AutoModelForImageClassification.from_pretrained("umm-maybe/ai-image-detector")

model.eval()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model.to(DEVICE)

print("Model running on:", next(model.parameters()).device)


# -----------------------------
# AI detector function
# -----------------------------
def ai_generated_image_score(frame: np.ndarray) -> float:
    """
    Returns probability [0.0 - 1.0] that image is AI-generated
    """
    # OpenCV → RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    inputs = processor(images=frame, return_tensors="pt")
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)

    # class index 1 = AI-generated
    ai_prob = probs[0, 1].item()
    return round(float(ai_prob), 3)


# -----------------------------
# LOCAL FILE TEST
# -----------------------------
if __name__ == "__main__":
    image_path = "C:/Users/vikram/OneDrive/Desktop/sampledata/aigen.jpeg"

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Could not read image file")

    score = ai_generated_image_score(img)

    print("\nAI Generated Probability:", score)

    if score >= 0.9:
        print("Verdict: ❌ LIKELY AI-GENERATED")
    elif score >= 0.7:
        print("Verdict: ⚠️ INCONCLUSIVE")
    else:
        print("Verdict: ✅ LIKELY REAL")
