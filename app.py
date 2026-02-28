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
    model     = joblib.load('model/placement_model.pkl')
    scaler    = joblib.load('model/scaler.pkl')
    le_branch = joblib.load('model/le_branch.pkl')
    le_gender = joblib.load('model/le_gender.pkl')
    features  = joblib.load('model/features.pkl')
    return model, scaler, le_branch, le_gender, features

model, scaler, le_branch, le_gender, features = load_model()

# ─────────────────────────────────────────
# NAVIGATION TABS
# ─────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🔮 Single Prediction",
    "📂 Bulk Prediction",
    "📊 Model Insights"
])

# ═════════════════════════════════════════
# TAB 1 — SINGLE PREDICTION
# ═════════════════════════════════════════
with tab1:
    st.title("🎓 Student Placement Prediction System")
    st.markdown("Predict whether a student will be placed and identify at-risk students.")
    st.divider()

    # SIDEBAR
    st.sidebar.header("📋 Enter Student Details")

    st.sidebar.subheader("🎓 Academic Information")
    ssc_percentage    = st.sidebar.slider("SSC Percentage (10th)", 40.0, 100.0, 70.0)
    hsc_percentage    = st.sidebar.slider("HSC Percentage (12th)", 40.0, 100.0, 70.0)
    degree_percentage = st.sidebar.slider("Degree Percentage",     40.0, 100.0, 70.0)
    cgpa              = st.sidebar.slider("CGPA",                   4.0,  10.0,  7.5)
    active_backlogs   = st.sidebar.number_input("Active Backlogs",   0,    10,    0)

    st.sidebar.subheader("💡 Skills & Assessment")
    aptitude_test_score       = st.sidebar.slider("Aptitude Test Score",       0.0, 100.0, 60.0)
    coding_test_score         = st.sidebar.slider("Coding Test Score",          0.0, 100.0, 60.0)
    technical_interview_score = st.sidebar.slider("Technical Interview Score",  0.0, 100.0, 60.0)
    communication_score       = st.sidebar.slider("Communication Score",        0.0, 100.0, 60.0)

    st.sidebar.subheader("🏆 Activities & Experience")
    internships_count       = st.sidebar.number_input("Internships Count",        0, 10, 0)
    projects_count          = st.sidebar.number_input("Projects Count",           0, 20, 2)
    certifications_count    = st.sidebar.number_input("Certifications Count",     0, 20, 1)
    hackathons_participated = st.sidebar.number_input("Hackathons Participated",  0, 20, 0)
    work_experience_months  = st.sidebar.number_input("Work Experience (months)", 0, 24, 0)

    st.sidebar.subheader("📊 Engagement")
    attendance_percentage         = st.sidebar.slider("Attendance Percentage", 40.0, 100.0, 80.0)
    extracurricular_participation = st.sidebar.selectbox("Extracurricular Participation", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    st.sidebar.subheader("👤 Personal Details")
    branch = st.sidebar.selectbox("Branch", ['CSE', 'IT', 'ECE', 'Mechanical', 'Civil'])
    gender = st.sidebar.selectbox("Gender", ['Male', 'Female'])

    # DERIVED FEATURES
    academic_score = (0.3 * ssc_percentage + 0.3 * hsc_percentage + 0.4 * degree_percentage)
    skill_score    = (aptitude_test_score + coding_test_score + technical_interview_score + communication_score) / 4
    activity_score = (internships_count + projects_count + certifications_count + hackathons_participated)

    # ENCODE
    try:
        branch_encoded = le_branch.transform([branch])[0]
    except:
        branch_encoded = 0
    try:
        gender_encoded = le_gender.transform([gender])[0]
    except:
        gender_encoded = 0

    predict_btn = st.sidebar.button("🔮 Predict Placement", use_container_width=True)

    # METRICS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Academic Score", f"{academic_score:.2f}")
    with col2:
        st.metric("Skill Score", f"{skill_score:.2f}")
    with col3:
        st.metric("Activity Score", f"{activity_score:.2f}")

    st.divider()

    if predict_btn:
        input_data = pd.DataFrame([{
            'ssc_percentage':               ssc_percentage,
            'hsc_percentage':               hsc_percentage,
            'degree_percentage':            degree_percentage,
            'cgpa':                         cgpa,
            'active_backlogs':              active_backlogs,
            'aptitude_test_score':          aptitude_test_score,
            'coding_test_score':            coding_test_score,
            'technical_interview_score':    technical_interview_score,
            'communication_score':          communication_score,
            'internships_count':            internships_count,
            'projects_count':               projects_count,
            'certifications_count':         certifications_count,
            'hackathons_participated':      hackathons_participated,
            'attendance_percentage':        attendance_percentage,
            'extracurricular_participation': extracurricular_participation,
            'work_experience_months':       work_experience_months,
            'branch':                       branch_encoded,
            'gender':                       gender_encoded,
            'academic_score':               academic_score,
            'skill_score':                  skill_score,
            'activity_score':               activity_score,
        }])

        input_data  = input_data[features]
        probability = model.predict_proba(input_data)[0][1]
        prediction  = model.predict(input_data)[0]

        if probability >= 0.6:
            risk_label = "🟢 Low Risk"
        elif probability >= 0.4:
            risk_label = "🟡 Medium Risk"
        else:
            risk_label = "🔴 High Risk"

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
            fig, ax  = plt.subplots(figsize=(5, 3))
            sns.barplot(x='Category', y='Score', data=score_df,
                        palette=['#4CAF50', '#2196F3', '#FF9800'], ax=ax)
            ax.set_ylim(0, 100)
            ax.set_title("Student Score Breakdown")
            st.pyplot(fig)
            plt.close()

        st.divider()
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
            st.write(f"Aptitude      : {aptitude_test_score}")
            st.write(f"Coding        : {coding_test_score}")
            st.write(f"Technical     : {technical_interview_score}")
            st.write(f"Communication : {communication_score}")

        with profile_col3:
            st.markdown("**Activity Details**")
            st.write(f"Internships    : {internships_count}")
            st.write(f"Projects       : {projects_count}")
            st.write(f"Certifications : {certifications_count}")
            st.write(f"Hackathons     : {hackathons_participated}")
            st.write(f"Attendance     : {attendance_percentage}%")

        st.divider()

# ═════════════════════════════════════════
# TAB 2 — BULK PREDICTION
# ═════════════════════════════════════════
with tab2:
    st.title("📂 Bulk Placement Prediction")
    st.markdown("Upload a CSV file with multiple students and predict placement for all at once.")
    st.divider()

    # ── Download Sample CSV ──
    st.subheader("📥 Step 1 — Download Sample CSV Template")
    sample_data = pd.DataFrame([{
        'ssc_percentage': 75.0,
        'hsc_percentage': 70.0,
        'degree_percentage': 72.0,
        'cgpa': 7.5,
        'active_backlogs': 0,
        'aptitude_test_score': 65.0,
        'coding_test_score': 70.0,
        'technical_interview_score': 68.0,
        'communication_score': 72.0,
        'internships_count': 1,
        'projects_count': 3,
        'certifications_count': 2,
        'hackathons_participated': 1,
        'attendance_percentage': 85.0,
        'extracurricular_participation': 1,
        'work_experience_months': 0,
        'branch': 'CSE',
        'gender': 'Male'
    }])

    csv_template = sample_data.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Sample CSV Template",
        data=csv_template,
        file_name="sample_students.csv",
        mime="text/csv"
    )

    st.divider()

    # ── Upload CSV ──
    st.subheader("📤 Step 2 — Upload Your Students CSV")
    uploaded_file = st.file_uploader("Upload CSV or Excel File", type=['csv', 'xlsx', 'xls'])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                bulk_df = pd.read_csv(uploaded_file)
            else:
                bulk_df = pd.read_excel(uploaded_file)
            st.success(f"✅ File uploaded successfully — {len(bulk_df)} students found")
            st.dataframe(bulk_df.head(), use_container_width=True)

            if st.button("🔮 Predict for All Students", use_container_width=True):

                results = []

                for _, row in bulk_df.iterrows():
                    try:
                        # Derived features
                        academic_score = (0.3 * row['ssc_percentage'] +
                                          0.3 * row['hsc_percentage'] +
                                          0.4 * row['degree_percentage'])
                        skill_score    = (row['aptitude_test_score'] +
                                          row['coding_test_score'] +
                                          row['technical_interview_score'] +
                                          row['communication_score']) / 4
                        activity_score = (row['internships_count'] +
                                          row['projects_count'] +
                                          row['certifications_count'] +
                                          row['hackathons_participated'])

                        # Encode
                        try:
                            branch_enc = le_branch.transform([row['branch']])[0]
                        except:
                            branch_enc = 0
                        try:
                            gender_enc = le_gender.transform([row['gender']])[0]
                        except:
                            gender_enc = 0

                        input_dict = {
                            'ssc_percentage':               row['ssc_percentage'],
                            'hsc_percentage':               row['hsc_percentage'],
                            'degree_percentage':            row['degree_percentage'],
                            'cgpa':                         row['cgpa'],
                            'active_backlogs':              row['active_backlogs'],
                            'aptitude_test_score':          row['aptitude_test_score'],
                            'coding_test_score':            row['coding_test_score'],
                            'technical_interview_score':    row['technical_interview_score'],
                            'communication_score':          row['communication_score'],
                            'internships_count':            row['internships_count'],
                            'projects_count':               row['projects_count'],
                            'certifications_count':         row['certifications_count'],
                            'hackathons_participated':      row['hackathons_participated'],
                            'attendance_percentage':        row['attendance_percentage'],
                            'extracurricular_participation': row['extracurricular_participation'],
                            'work_experience_months':       row['work_experience_months'],
                            'branch':                       branch_enc,
                            'gender':                       gender_enc,
                            'academic_score':               academic_score,
                            'skill_score':                  skill_score,
                            'activity_score':               activity_score,
                        }

                        input_df    = pd.DataFrame([input_dict])[features]
                        probability = model.predict_proba(input_df)[0][1]
                        prediction  = model.predict(input_df)[0]

                        if probability >= 0.6:
                            risk = "🟢 Low Risk"
                        elif probability >= 0.4:
                            risk = "🟡 Medium Risk"
                        else:
                            risk = "🔴 High Risk"

                        results.append({
                            'Branch':              row['branch'],
                            'Gender':              row['gender'],
                            'CGPA':                row['cgpa'],
                            'Placement':           '✅ Placed' if prediction == 1 else '❌ Not Placed',
                            'Probability (%)':     round(probability * 100, 2),
                            'Risk Level':          risk,
                            'Academic Score':      round(academic_score, 2),
                            'Skill Score':         round(skill_score, 2),
                            'Activity Score':      round(activity_score, 2),
                        })

                    except Exception as e:
                        results.append({'Error': str(e)})

                results_df = pd.DataFrame(results)

                st.divider()
                st.subheader("📊 Prediction Results")
                st.dataframe(results_df, use_container_width=True)

                # Summary
                st.divider()
                st.subheader("📈 Summary")
                total    = len(results_df)
                placed   = len(results_df[results_df['Placement'] == '✅ Placed'])
                not_placed = total - placed
                high_risk  = len(results_df[results_df['Risk Level'] == '🔴 High Risk'])

                sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
                with sum_col1:
                    st.metric("Total Students", total)
                with sum_col2:
                    st.metric("Likely Placed", placed)
                with sum_col3:
                    st.metric("At Risk", not_placed)
                with sum_col4:
                    st.metric("High Risk Students", high_risk)

                # Pie chart
                fig, ax = plt.subplots(figsize=(4, 4))
                ax.pie(
                    [placed, not_placed],
                    labels=['Placed', 'Not Placed'],
                    autopct='%1.1f%%',
                    colors=['#4CAF50', '#F44336']
                )
                ax.set_title("Placement Distribution")
                st.pyplot(fig)
                plt.close()

                # Download results
                st.divider()
                st.subheader("⬇️ Download Results")
                result_csv = results_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Prediction Results CSV",
                    data=result_csv,
                    file_name="placement_predictions.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
            st.info("Make sure your CSV matches the sample template format.")

# ═════════════════════════════════════════
# TAB 3 — MODEL INSIGHTS
# ═════════════════════════════════════════
with tab3:
    st.title("📊 Model Insights")
    st.divider()

    st.subheader("📈 Feature Importance (Random Forest)")
    if os.path.exists("model/feature_importance.png"):
        img = Image.open("model/feature_importance.png")
        st.image(img, caption="Feature Importance", use_container_width=True)
    else:
        st.info("Feature importance chart will appear after training.")

    st.divider()

    st.subheader("🔢 Confusion Matrix (Random Forest)")
    if os.path.exists("model/confusion_matrix.png"):
        img2 = Image.open("model/confusion_matrix.png")
        st.image(img2, caption="Confusion Matrix", use_container_width=True)
    else:
        st.info("Confusion matrix will appear after training.")

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.divider()
st.markdown("Built with ❤️ using Streamlit + Random Forest | Placement Prediction System")