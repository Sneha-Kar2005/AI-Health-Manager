# app.py - Streamlit frontend for AI Health Manager
import streamlit as st
from dotenv import load_dotenv
from gemini_client import analyze_food_image, generate_meal_plan, model
from utils import load_image_from_bytes


st.set_page_config(page_title="AI Health Manager", layout="centered")
st.title("AI-Powered Health Management System")

# Sidebar: user profile input
st.sidebar.header("Your health profile")
with st.sidebar.form("profile_form"):
    age = st.number_input("Age", min_value=5, max_value=120, value=28)
    sex = st.selectbox("Sex", ["Female", "Male", "Other"])
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=80.0, max_value=250.0, value=170.0)
    activity = st.selectbox("Activity level", ["Sedentary","Light","Moderate","Active","Very active"])
    goal = st.selectbox("Goal", ["Maintain weight","Lose weight","Gain weight"])
    allergies = st.text_input("Allergies / dietary restrictions (comma separated)")
    preferences = st.text_input("Preferences (e.g. vegetarian, low-carb)")
    days = st.slider("Meal plan days", 1, 14, 3)
    submitted = st.form_submit_button("Save profile")
if submitted:
    st.success("Profile saved (temporary; implement DB to persist).")

# ✅ Unified profile keys
user_profile = {
    "age": age,
    "sex": sex,
    "weight": weight,
    "height": height,
    "activity_level": activity,
    "goal": goal,
    "restrictions": allergies,
    "preferences": preferences,
}

# Meal planner
st.header("Generate personalized meal plan")
if st.button("Generate meal plan"):
    try:
        with st.spinner("Generating meal plan..."):
            plan_text = generate_meal_plan(user_profile, days=days)

        st.subheader("📅 Personalized Meal Plan")

        if "Day 1" in plan_text:
            # Split into structured days
            days_split = plan_text.split("Day ")
            for d in days_split:
                if d.strip() == "" or not d[0].isdigit():
                    continue
                try:
                    day_num, meals = d.split("\n", 1)
                    st.markdown(f"### 🌟 Day {day_num.strip()}")

                    # Create dict for meals
                    meal_dict = {"Breakfast": "", "Lunch": "", "Dinner": "", "Snacks": ""}

                    for line in meals.split("\n"):
                        line = line.strip()
                        if line.lower().startswith("breakfast"):
                            meal_dict["Breakfast"] = line.split(":", 1)[-1].strip()
                        elif line.lower().startswith("lunch"):
                            meal_dict["Lunch"] = line.split(":", 1)[-1].strip()
                        elif line.lower().startswith("dinner"):
                            meal_dict["Dinner"] = line.split(":", 1)[-1].strip()
                        elif line.lower().startswith("snack"):
                            meal_dict["Snacks"] = line.split(":", 1)[-1].strip()

                    df = pd.DataFrame([meal_dict])
                    st.table(df)

                except Exception:
                    st.markdown(meals.replace("-", "•"))
                st.markdown("---")
        else:
            # Fallback: show raw plan text
            st.markdown(plan_text)

    except Exception as e:
        st.error(f"Error generating meal plan: {e}")

# Food image analysis
st.header("Analyze food from image")
uploaded = st.file_uploader("Upload food photo", type=["jpg","jpeg","png"])
if uploaded is not None:
    try:
        img = load_image_from_bytes(uploaded)
        st.image(img, caption="Uploaded image", use_column_width=True)
        if st.button("Analyze food"):
            with st.spinner("Analyzing image..."):
                result = analyze_food_image(img)
            st.markdown("**Analysis result:**")
            st.write(result)
    except Exception as e:
        st.error(f"Error analyzing image: {e}")

# Simple health Q&A
st.header("Ask a health question")
q = st.text_area("Enter a health-related question (nutrition, exercise, meal ideas)")
if st.button("Ask AI"):
    if not q.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Generating answer..."):
                prompt = (
                    "You are a helpful, evidence-based health advisor. "
                    "Answer concisely and cite well-known guidelines when appropriate.\n\n"
                    f"Question: {q}\n\nProvide a short answer and practical recommendations."
                )
                resp = text_model.generate_content(prompt)
                st.markdown("**Answer:**")
                st.write(resp.text or resp)
        except Exception as e:
            st.error(f"Error getting answer: {e}")
