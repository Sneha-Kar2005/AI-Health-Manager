# app.py - Streamlit frontend for AI Health Manager
import streamlit as st
from dotenv import load_dotenv
from gemini_client import analyze_food_image, generate_meal_plan, model
from utils import load_image_from_bytes

load_dotenv()

st.set_page_config(page_title="AI Health Manager", layout="centered")
st.title("AI-Powered Health Management System")

# ✅ Show which Gemini model was selected (from gemini_client.py)
st.sidebar.info(f"🔮 Using Gemini model: **{model.model_name}**")

# Sidebar: user profile input
st.sidebar.header("Your health profile")
with st.sidebar.form("profile_form"):
    age = st.number_input("Age", min_value=5, max_value=120, value=28)
    sex = st.selectbox("Sex", ["Female", "Male", "Other"])
    weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=80.0, max_value=250.0, value=170.0)
    activity = st.selectbox("Activity level", ["Sedentary", "Light", "Moderate", "Active", "Very active"])
    goal = st.selectbox("Goal", ["Maintain weight", "Lose weight", "Gain weight"])
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

# ----------------------
# Meal planner
# ----------------------
st.header("Generate personalized meal plan")
if st.button("Generate meal plan"):
    try:
        with st.spinner("Generating meal plan..."):
            plan = generate_meal_plan(user_profile, days=days)
        st.subheader("📅 Personalized Meal Plan")
        st.markdown(plan if isinstance(plan, str) else str(plan))
    except Exception as e:
        st.error(f"❌ Error generating meal plan: {e}")

# ----------------------
# Food image analysis
# ----------------------
st.header("Analyze food from image")
uploaded = st.file_uploader("Upload food photo", type=["jpg", "jpeg", "png"])
if uploaded is not None:
    try:
        img = load_image_from_bytes(uploaded)
        st.image(img, caption="Uploaded image", use_column_width=True)
        if st.button("Analyze food"):
            with st.spinner("Analyzing image..."):
                result = analyze_food_image(img)
            st.markdown("**🍽️ Analysis result:**")
            st.write(result)
    except Exception as e:
        st.error(f"❌ Error analyzing image: {e}")

# ----------------------
# Health Q&A
# ----------------------
st.header("Ask a health question")
q = st.text_area("Enter a health-related question (nutrition, exercise, meal ideas)")
if st.button("Ask AI"):
    if not q.strip():
        st.warning("⚠️ Please enter a question.")
    else:
        try:
            with st.spinner("Thinking..."):
                prompt = (
                    "You are a helpful, evidence-based health advisor. "
                    "Answer concisely and cite well-known guidelines when appropriate.\n\n"
                    f"Question: {q}\n\nProvide a short answer and practical recommendations."
                )
                resp = model.generate_content(prompt)
                st.markdown("**💡 Answer:**")
                st.write(resp.text or resp)
        except Exception as e:
            st.error(f"❌ Error getting answer: {e}")
