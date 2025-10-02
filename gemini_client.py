import streamlit as st
import google.generativeai as genai

# Load API key from Streamlit Cloud Secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception as e:
    raise ValueError("❌ GOOGLE_API_KEY not found. Please add it in Streamlit Secrets.")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Function to analyze food image
def analyze_food_image(image_file):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(["Analyze the nutritional content of this food.", image_file])
    return response.text

# Function to generate personalized meal plan
def generate_meal_plan(profile):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Create a personalized meal plan for:
    Age: {profile['age']}, Sex: {profile['sex']}, 
    Weight: {profile['weight']} kg, Height: {profile['height']} cm,
    Activity level: {profile['activity_level']}, Goal: {profile['goal']},
    Allergies/restrictions: {profile['restrictions']}
    """
    response = model.generate_content(prompt)
    return response.text

