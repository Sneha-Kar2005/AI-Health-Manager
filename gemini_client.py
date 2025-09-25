# gemini_client.py
import os
from PIL import Image
import re
import json

try:
    import google.generativeai as genai
except Exception as e:
    raise ImportError("google.generativeai is required. Install via `pip install google-genai`.") from e

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GEMINI_API_KEY or GOOGLE_API_KEY in environment.")
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


def analyze_food_image(pil_image: Image.Image, extra_prompt: str = "") -> dict:
    """
    Send an image + prompt to Gemini and parse a structured response.
    Returns a dict with keys like: estimated_calories, ingredients, confidence, nutrition_breakdown
    If the model cannot produce JSON, returns {'raw': <text>}
    """
    prompt_text = (
        "You are a professional nutrition analyst. Given this food image, do the following:\n"
        "1) Identify the most likely dish name and main ingredients.\n"
        "2) Provide an estimated portion size and estimated calories with reasoning (clearly show assumptions).\n"
        "3) Provide a brief macronutrient estimate (carbs/protein/fat grams).\n"
        "4) Output a JSON object with keys: dish, ingredients (list), estimated_calories (number), "
        "macros (dict), confidence_score (0-1).\n"
        + extra_prompt
    )

    # Many SDKs accept a list of contents where images are passed inline.
    # We'll use generate_content; the SDK may vary; adapt if necessary.
    resp = model.generate_content([prompt_text, pil_image])
    text = resp.text or ""

    # Try to extract JSON blob
    jmatch = re.search(r"(\{.*\})", text, re.S)
    if jmatch:
        try:
            return json.loads(jmatch.group(1))
        except Exception:
            pass
    # fallback: return raw text
    return {"raw": text}


def generate_meal_plan(user_profile: dict, days: int = 3) -> dict:
    """
    Generate a meal plan as JSON for the provided user_profile.
    user_profile: dict with keys age, sex, weight_kg, height_cm, activity_level, goals, allergies, preferences
    Returns parsed JSON or {'raw': <text>} on failure.
    """
    profile_text = "\n".join(f"{k}: {v}" for k, v in user_profile.items())
    prompt = (
        f"You are a certified dietitian. Create a {days}-day meal plan for the following user:\n"
        f"{profile_text}\n\n"
        "For each day provide: breakfast, lunch, snack, dinner. For each meal provide dish, estimated calories, "
        "macronutrient breakdown (carbs/protein/fat grams), and substitutions for allergies/preferences. "
        "Output valid JSON with top-level key 'days' which is a list of day objects."
    )
    resp = model.generate_content(prompt)
    text = resp.text or ""
    # Extract JSON
    jmatch = re.search(r"(\{.*\})", text, re.S)
    if jmatch:
        try:
            return json.loads(jmatch.group(1))
        except Exception:
            pass
    return {"raw": text}
