import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Use secrets on cloud, .env locally
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please set it in .env (local) or Streamlit Secrets (cloud).")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_food_image(image_file):
    response = model.generate_content(["Analyze the nutritional content of this food.", image_file])
    return response.text

def generate_meal_plan(profile, days=3):
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
