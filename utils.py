# utils.py
from PIL import Image
import io

def load_image_from_bytes(uploaded_file):
    """
    Accepts a Streamlit UploadedFile or bytes file-like object and returns a PIL Image (RGB).
    """
    img = Image.open(uploaded_file)
    return img.convert("RGB")

def heuristic_calorie_adjust(base_calories, portion_multiplier=1.0):
    return int(base_calories * portion_multiplier)
