import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file (local development only)
load_dotenv()

# First check Streamlit Secrets (for cloud)
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please set it in .env (local) or Streamlit Secrets (cloud).")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Reuse model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to analyze food image
def analyze_food_image(image_file):
    response = model.generate_content(["Analyze the nutritional content of this food.", image_file])
    return response.text

# Function to generate personalized meal plan
def generate_meal_plan(profile, days=3):
    prompt = f"""
    Create a personalized {days}-day meal plan.

    Profile:
    Age: {profile['age']}, Sex: {profile['sex']},
    Weight: {profile['weight_kg']} kg, Height: {profile['height_cm']} cm,
    Activity level: {profile['activity_level']}, Goal: {profile['goals']},
    Allergies/restrictions: {profile['allergies']}, Preferences: {profile['preferences']}
    """
    response = model.generate_content(prompt)
    return response.text
