import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables for local use
load_dotenv()

# Try secrets first (cloud), then .env (local)
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please set it in .env (local) or Streamlit Secrets (cloud).")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Define models
text_model = genai.GenerativeModel("gemini-1.5-pro")         # For meal plans / text tasks
vision_model = genai.GenerativeModel("gemini-1.5-pro-vision") # For food image analysis

# Function: analyze food image
def analyze_food_image(image_file):
    try:
        response = vision_model.generate_content(
            ["Analyze the nutritional content of this food. Provide calories, macros, and a short description.", image_file]
        )
        return response.text
    except Exception as e:
        return f"❌ Error analyzing food image: {e}"

# Function: generate personalized meal plan
def generate_meal_plan(profile, days=3):
    try:
        prompt = f"""
        Create a personalized {days}-day meal plan.

        Profile:
        Age: {profile['age']}, Sex: {profile['sex']},
        Weight: {profile['weight']} kg, Height: {profile['height']} cm,
        Activity level: {profile['activity_level']}, Goal: {profile['goal']},
        Allergies/restrictions: {profile['restrictions']}, Preferences: {profile['preferences']}

        Format the output in a structured way:
        - Day 1
          - Breakfast: ...
          - Lunch: ...
          - Dinner: ...
          - Snacks: ...
        """
        response = text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating meal plan: {e}"
