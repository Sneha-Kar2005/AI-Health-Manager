import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env for local dev
load_dotenv()

# Get API key (first from Streamlit secrets, fallback to local .env)
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please set it in Streamlit secrets or .env file.")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Auto-select best available model
def get_best_model():
    try:
        models = [m for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
        # Prefer latest stable models
        preferred_order = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro", "gemini-1.0-pro-vision"]
        for name in preferred_order:
            for m in models:
                if name in m.name:
                    print(f"✅ Using model: {m.name}")
                    return genai.GenerativeModel(m.name)
        # fallback
        if models:
            print(f"⚠️ Using fallback model: {models[0].name}")
            return genai.GenerativeModel(models[0].name)
        else:
            raise RuntimeError("❌ No available Gemini models found for your API key.")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch models: {e}")

# Create model instance
model = get_best_model()

# -----------------------
# Functions
# -----------------------

def analyze_food_image(image_file):
    """Analyze nutritional content from an uploaded image."""
    response = model.generate_content(
        ["Analyze the nutritional content of this food image.", image_file]
    )
    return response.text

def generate_meal_plan(profile, days=3):
    """Generate a personalized meal plan."""
    prompt = f"""
    Create a personalized {days}-day meal plan.

    Profile:
    Age: {profile['age']}, Sex: {profile['sex']},
    Weight: {profile['weight']} kg, Height: {profile['height']} cm,
    Activity level: {profile['activity_level']}, Goal: {profile['goal']},
    Allergies/restrictions: {profile['restrictions']}, Preferences: {profile['preferences']}
    """
    response = model.generate_content(prompt)
    return response.text
