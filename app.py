import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Placement Prediction System",
    page_icon="🎓",
    layout="wide"
)

# ─────────────────────────────────────────
# LOAD MODEL & ENCODERS
# ─────────────────────────────────────────
@st.cache_resource
def load_model():
    model    = joblib.load('model/placement_model.pkl')
    scaler   = joblib.load('model/scaler.pkl')
    le_branch = joblib.load('model/le_branch.pkl')
    le_gender = joblib.load('model/le_gender.pkl')
    features  = joblib.load('model/features.pkl')
    return model, scaler, le_branch, le_gender, features

model, scaler, le_branch, le_gender, features = load_model()

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("🎓 Student Placement Prediction System")
st.markdown("Predict whether a student will be placed and identify at-risk students.")
st.divider()

# ─────────────────────────────────────────
# SIDEBAR — STUDENT INPUT FORM
# ─────────────────────────────────────────
st.sidebar.header("📋 Enter Student Details")

st.sidebar.subheader("🎓 Academic Information")
ssc_percentage   = st.sidebar.slider("SSC Percentage (10th)", 40.0, 100.0, 70.0)
hsc_percentage   = st.sidebar.slider("HSC Percentage (12th)", 40.0, 100.0, 70.0)
degree_percentage = st.sidebar.slider("Degree Percentage",    40.0, 100.0, 70.0)
cgpa             = st.sidebar.slider("CGPA",                   4.0,  10.0,  7.5)
active_backlogs  = st.sidebar.number_input("Active Backlogs",   0,    10,    0)

st.sidebar.subheader("💡 Skills & Assessment")
aptitude_test_score       = st.sidebar.slider("Aptitude Test Score",        0.0, 100.0, 60.0)
coding_test_score         = st.sidebar.slider("Coding Test Score",           0.0, 100.0, 60.0)
technical_interview_score = st.sidebar.slider("Technical Interview Score",   0.0, 100.0, 60.0)
communication_score       = st.sidebar.slider("Communication Score",         0.0, 100.0, 60.0)

st.sidebar.subheader("🏆 Activities & Experience")
internships_count      = st.sidebar.number_input("Internships Count",         0, 10, 0)
projects_count         = st.sidebar.number_input("Projects Count",            0, 20, 2)
certifications_count   = st.sidebar.number_input("Certifications Count",      0, 20, 1)
hackathons_participated = st.sidebar.number_input("Hackathons Participated",  0, 20, 0)
work_experience_months = st.sidebar.number_input("Work Experience (months)",  0, 24, 0)

st.sidebar.subheader("📊 Engagement")
attendance_percentage        = st.sidebar.slider("Attendance Percentage", 40.0, 100.0, 80.0)
extracurricular_participation = st.sidebar.selectbox("Extracurricular Participation", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

st.sidebar.subheader("👤 Personal Details")
branch = st.sidebar.selectbox("Branch", ['CSE', 'IT', 'ECE', 'Mechanical', 'Civil'])
gender = st.sidebar.selectbox("Gender", ['Male', 'Female'])

# ─────────────────────────────────────────
# DERIVED FEATURES
# ─────────────────────────────────────────
academic_score = (
    0.3 * ssc_percentage +
    0.3 * hsc_percentage +
    0.4 * degree_percentage
)

skill_score = (
    aptitude_test_score +
    coding_test_score +
    technical_interview_score +
    communication_score
) / 4

activity_score = (
    internships_count +
    projects_count +
    certifications_count +
    hackathons_participated
)

# ─────────────────────────────────────────
# ENCODE CATEGORICAL
# ─────────────────────────────────────────
try:
    branch_encoded = le_branch.transform([branch])[0]
except:
    branch_encoded = 0

try:
    gender_encoded = le_gender.transform([gender])[0]
except:
    gender_encoded = 0

# ─────────────────────────────────────────
# PREDICT BUTTON
# ─────────────────────────────────────────
predict_btn = st.sidebar.button("🔮 Predict Placement", use_container_width=True)

# ─────────────────────────────────────────
# MAIN LAYOUT — 3 COLUMNS
# ─────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Academic Score",  f"{academic_score:.2f}")
with col2:
    st.metric("Skill Score",     f"{skill_score:.2f}")
with col3:
    st.metric("Activity Score",  f"{activity_score:.2f}")

st.divider()

# ─────────────────────────────────────────
# PREDICTION RESULT
# ─────────────────────────────────────────
if predict_btn:

    input_data = pd.DataFrame([{
        'ssc_percentage':              ssc_percentage,
        'hsc_percentage':              hsc_percentage,
        'degree_percentage':           degree_percentage,
        'cgpa':                        cgpa,
        'active_backlogs':             active_backlogs,
        'aptitude_test_score':         aptitude_test_score,
        'coding_test_score':           coding_test_score,
        'technical_interview_score':   technical_interview_score,
        'communication_score':         communication_score,
        'internships_count':           internships_count,
        'projects_count':              projects_count,
        'certifications_count':        certifications_count,
        'hackathons_participated':     hackathons_participated,
        'attendance_percentage':       attendance_percentage,
        'extracurricular_participation': extracurricular_participation,
        'work_experience_months':      work_experience_months,
        'branch':                      branch_encoded,
        'gender':                      gender_encoded,
        'academic_score':              academic_score,
        'skill_score':                 skill_score,
        'activity_score':              activity_score,
    }])

    input_data = input_data[features]

    probability = model.predict_proba(input_data)[0][1]
    prediction  = model.predict(input_data)[0]

    # Risk Label
    if probability >= 0.6:
        risk_label = "🟢 Low Risk"
        risk_color = "green"
    elif probability >= 0.4:
        risk_label = "🟡 Medium Risk"
        risk_color = "orange"
    else:
        risk_label = "🔴 High Risk"
        risk_color = "red"

    # Result Display
    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.subheader("🔮 Prediction Result")
        if prediction == 1:
            st.success("✅ Student is likely to be PLACED")
        else:
            st.error("❌ Student is at risk of NOT being placed")

        st.markdown(f"**Placement Probability:** `{probability * 100:.2f}%`")
        st.progress(float(probability))
        st.markdown(f"**Risk Level:** {risk_label}")

    with res_col2:
        st.subheader("📊 Score Summary")
        score_data = {
            'Category': ['Academic', 'Skill', 'Activity'],
            'Score':    [academic_score, skill_score, activity_score]
        }
        score_df = pd.DataFrame(score_data)
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.barplot(x='Category', y='Score', data=score_df,
                    palette=['#4CAF50', '#2196F3', '#FF9800'], ax=ax)
        ax.set_ylim(0, 100)
        ax.set_title("Student Score Breakdown")
        st.pyplot(fig)
        plt.close()

    st.divider()

    # Student Profile Summary
    st.subheader("📋 Student Profile Summary")
    profile_col1, profile_col2, profile_col3 = st.columns(3)

    with profile_col1:
        st.markdown("**Academic Details**")
        st.write(f"SSC      : {ssc_percentage}%")
        st.write(f"HSC      : {hsc_percentage}%")
        st.write(f"Degree   : {degree_percentage}%")
        st.write(f"CGPA     : {cgpa}")
        st.write(f"Backlogs : {active_backlogs}")

    with profile_col2:
        st.markdown("**Skill Details**")
        st.write(f"Aptitude    : {aptitude_test_score}")
        st.write(f"Coding      : {coding_test_score}")
        st.write(f"Technical   : {technical_interview_score}")
        st.write(f"Communication: {communication_score}")

    with profile_col3:
        st.markdown("**Activity Details**")
        st.write(f"Internships    : {internships_count}")
        st.write(f"Projects       : {projects_count}")
        st.write(f"Certifications : {certifications_count}")
        st.write(f"Hackathons     : {hackathons_participated}")
        st.write(f"Attendance     : {attendance_percentage}%")

    st.divider()

# ─────────────────────────────────────────
# FEATURE IMPORTANCE SECTION
# ─────────────────────────────────────────
st.subheader("📈 Feature Importance (Random Forest)")

if os.path.exists("model/feature_importance.png"):
    img = Image.open("model/feature_importance.png")
    st.image(img, caption="Feature Importance", use_column_width=True)
else:
    st.info("Feature importance chart will appear after training.")

# ─────────────────────────────────────────
# CONFUSION MATRIX SECTION
# ─────────────────────────────────────────
st.subheader("🔢 Confusion Matrix (Random Forest)")

if os.path.exists("model/confusion_matrix.png"):
    img2 = Image.open("model/confusion_matrix.png")
    st.image(img2, caption="Confusion Matrix", use_column_width=True)
else:
    st.info("Confusion matrix will appear after training.")

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.divider()
st.markdown("Built with ❤️ using Streamlit + Random Forest | Placement Prediction System")