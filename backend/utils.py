import pandas as pd
import numpy as np
import joblib
import os

# ─────────────────────────────────────────
# LOAD ALL SAVED MODEL FILES
# ─────────────────────────────────────────
def load_all_models():
    """
    Load model, scaler, encoders and feature list
    from the model folder
    """
    model     = joblib.load('model/placement_model.pkl')
    scaler    = joblib.load('model/scaler.pkl')
    le_branch = joblib.load('model/le_branch.pkl')
    le_gender = joblib.load('model/le_gender.pkl')
    features  = joblib.load('model/features.pkl')

    return model, scaler, le_branch, le_gender, features


# ─────────────────────────────────────────
# COMPUTE DERIVED FEATURES
# ─────────────────────────────────────────
def compute_derived_features(data: dict) -> dict:
    """
    Takes raw input dictionary and adds
    academic_score, skill_score, activity_score
    """
    data['academic_score'] = (
        0.3 * data['ssc_percentage'] +
        0.3 * data['hsc_percentage'] +
        0.4 * data['degree_percentage']
    )

    data['skill_score'] = (
        data['aptitude_test_score'] +
        data['coding_test_score'] +
        data['technical_interview_score'] +
        data['communication_score']
    ) / 4

    data['activity_score'] = (
        data['internships_count'] +
        data['projects_count'] +
        data['certifications_count'] +
        data['hackathons_participated']
    )

    return data


# ─────────────────────────────────────────
# ENCODE CATEGORICAL FEATURES
# ─────────────────────────────────────────
def encode_categoricals(data: dict, le_branch, le_gender) -> dict:
    """
    Encode branch and gender using saved label encoders
    """
    try:
        data['branch'] = le_branch.transform([data['branch']])[0]
    except Exception:
        data['branch'] = 0

    try:
        data['gender'] = le_gender.transform([data['gender']])[0]
    except Exception:
        data['gender'] = 0

    return data


# ─────────────────────────────────────────
# PREPARE INPUT DATAFRAME
# ─────────────────────────────────────────
def prepare_input(data: dict, features: list) -> pd.DataFrame:
    """
    Convert input dictionary to a
    properly ordered DataFrame for prediction
    """
    df = pd.DataFrame([data])
    df = df[features]
    return df


# ─────────────────────────────────────────
# GET RISK LABEL
# ─────────────────────────────────────────
def get_risk_label(probability: float) -> dict:
    """
    Returns risk label, color and message
    based on placement probability
    """
    if probability >= 0.6:
        return {
            'label':   '🟢 Low Risk',
            'color':   'green',
            'message': 'Student has a strong chance of getting placed.',
            'level':   'low'
        }
    elif probability >= 0.4:
        return {
            'label':   '🟡 Medium Risk',
            'color':   'orange',
            'message': 'Student needs improvement in some areas.',
            'level':   'medium'
        }
    else:
        return {
            'label':   '🔴 High Risk',
            'color':   'red',
            'message': 'Student is at high risk. Immediate attention needed.',
            'level':   'high'
        }


# ─────────────────────────────────────────
# GET IMPROVEMENT SUGGESTIONS
# ─────────────────────────────────────────
def get_suggestions(data: dict) -> list:
    """
    Returns list of improvement suggestions
    based on student weak areas
    """
    suggestions = []

    if data['cgpa'] < 7.0:
        suggestions.append("📚 Improve CGPA — aim for 7.5 or above")

    if data['active_backlogs'] > 0:
        suggestions.append("⚠️ Clear all active backlogs as soon as possible")

    if data['coding_test_score'] < 50:
        suggestions.append("💻 Practice coding — focus on DSA and problem solving")

    if data['aptitude_test_score'] < 50:
        suggestions.append("🧠 Improve aptitude skills — practice quantitative problems")

    if data['communication_score'] < 50:
        suggestions.append("🗣️ Work on communication skills — join public speaking clubs")

    if data['internships_count'] == 0:
        suggestions.append("🏢 Try to get at least one internship before placements")

    if data['certifications_count'] < 2:
        suggestions.append("📜 Get certified — try platforms like Coursera or NPTEL")

    if data['attendance_percentage'] < 75:
        suggestions.append("📅 Improve attendance — maintain at least 75%")

    if data['projects_count'] < 2:
        suggestions.append("🛠️ Build more projects to strengthen your portfolio")

    if data['hackathons_participated'] == 0:
        suggestions.append("🏆 Participate in at least one hackathon for experience")

    if not suggestions:
        suggestions.append("✅ Great profile! Keep maintaining your performance.")

    return suggestions


# ─────────────────────────────────────────
# FULL PREDICTION PIPELINE
# ─────────────────────────────────────────
def predict_placement(raw_input: dict) -> dict:
    """
    Complete prediction pipeline:
    1. Compute derived features
    2. Encode categoricals
    3. Prepare dataframe
    4. Predict
    5. Return full result
    """
    model, scaler, le_branch, le_gender, features = load_all_models()

    # Derived features
    data = compute_derived_features(raw_input.copy())

    # Encode
    data = encode_categoricals(data, le_branch, le_gender)

    # Prepare input
    input_df = prepare_input(data, features)

    # Predict
    probability = model.predict_proba(input_df)[0][1]
    prediction  = model.predict(input_df)[0]

    # Risk
    risk = get_risk_label(probability)

    # Suggestions
    suggestions = get_suggestions(data)

    return {
        'prediction':  int(prediction),
        'probability': round(float(probability) * 100, 2),
        'risk':        risk,
        'suggestions': suggestions,
        'scores': {
            'academic_score':  round(data['academic_score'], 2),
            'skill_score':     round(data['skill_score'], 2),
            'activity_score':  round(data['activity_score'], 2),
        }
    }


# ─────────────────────────────────────────
# VALIDATE INPUT DATA
# ─────────────────────────────────────────
def validate_input(data: dict) -> tuple:
    """
    Validates input data ranges
    Returns (is_valid, error_message)
    """
    errors = []

    if not (0 <= data['ssc_percentage'] <= 100):
        errors.append("SSC percentage must be between 0 and 100")

    if not (0 <= data['hsc_percentage'] <= 100):
        errors.append("HSC percentage must be between 0 and 100")

    if not (0 <= data['degree_percentage'] <= 100):
        errors.append("Degree percentage must be between 0 and 100")

    if not (0 <= data['cgpa'] <= 10):
        errors.append("CGPA must be between 0 and 10")

    if not (0 <= data['attendance_percentage'] <= 100):
        errors.append("Attendance must be between 0 and 100")

    if errors:
        return False, errors

    return True, []