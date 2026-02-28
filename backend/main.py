from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import io

# ─────────────────────────────────────────
# INIT APP
# ─────────────────────────────────────────
app = FastAPI(title="Placement Prediction API")

# ─────────────────────────────────────────
# CORS — Allow React to talk to FastAPI
# ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────
model     = joblib.load('model/placement_model.pkl')
scaler    = joblib.load('model/scaler.pkl')
le_branch = joblib.load('model/le_branch.pkl')
le_gender = joblib.load('model/le_gender.pkl')
features  = joblib.load('model/features.pkl')

# ─────────────────────────────────────────
# INPUT SCHEMA
# ─────────────────────────────────────────
class StudentInput(BaseModel):
    ssc_percentage:                float
    hsc_percentage:                float
    degree_percentage:             float
    cgpa:                          float
    active_backlogs:               int
    aptitude_test_score:           float
    coding_test_score:             float
    technical_interview_score:     float
    communication_score:           float
    internships_count:             int
    projects_count:                int
    certifications_count:          int
    hackathons_participated:       int
    attendance_percentage:         float
    extracurricular_participation: int
    work_experience_months:        int
    branch:                        str
    gender:                        str

# ─────────────────────────────────────────
# HELPER — PROCESS STUDENT DATA
# ─────────────────────────────────────────
def process_student(data: dict) -> dict:
    # Derived features
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

    # Encode categoricals
    try:
        data['branch'] = int(le_branch.transform([data['branch']])[0])
    except:
        data['branch'] = 0
    try:
        data['gender'] = int(le_gender.transform([data['gender']])[0])
    except:
        data['gender'] = 0

    return data

# ─────────────────────────────────────────
# HELPER — PREDICT
# ─────────────────────────────────────────
def predict(data: dict) -> dict:
    input_df    = pd.DataFrame([data])[features]
    probability = float(model.predict_proba(input_df)[0][1])
    prediction  = int(model.predict(input_df)[0])

    if probability >= 0.6:
        risk = "Low Risk"
    elif probability >= 0.4:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    return {
        "prediction":  prediction,
        "probability": round(probability * 100, 2),
        "risk":        risk,
        "placed":      prediction == 1,
        "scores": {
            "academic_score":  round(data['academic_score'], 2),
            "skill_score":     round(data['skill_score'], 2),
            "activity_score":  round(data['activity_score'], 2),
        }
    }

# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Placement Prediction API is running"}

# Single Prediction
@app.post("/predict")
def predict_single(student: StudentInput):
    data   = student.dict()
    data   = process_student(data)
    result = predict(data)
    return result

# Bulk Prediction
@app.post("/predict/bulk")
async def predict_bulk(file: UploadFile = File(...)):
    contents = await file.read()

    if file.filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    else:
        df = pd.read_excel(io.BytesIO(contents))

    results = []

    for _, row in df.iterrows():
        try:
            data   = row.to_dict()
            data   = process_student(data)
            result = predict(data)
            result['branch'] = str(row.get('branch', 'N/A'))
            result['gender'] = str(row.get('gender', 'N/A'))
            result['cgpa']   = float(row.get('cgpa', 0))
            results.append(result)
        except Exception as e:
            results.append({"error": str(e)})

    total      = len(results)
    placed     = sum(1 for r in results if r.get('placed', False))
    high_risk  = sum(1 for r in results if r.get('risk') == 'High Risk')

    return {
        "results":   results,
        "summary": {
            "total":      total,
            "placed":     placed,
            "not_placed": total - placed,
            "high_risk":  high_risk,
        }
    }

# Compare Two Students
@app.post("/compare")
def compare_students(student1: StudentInput, student2: StudentInput):
    data1   = process_student(student1.dict())
    data2   = process_student(student2.dict())
    result1 = predict(data1)
    result2 = predict(data2)

    if result1['probability'] > result2['probability']:
        verdict = f"Student 1 has higher placement probability by {round(result1['probability'] - result2['probability'], 2)}%"
    elif result2['probability'] > result1['probability']:
        verdict = f"Student 2 has higher placement probability by {round(result2['probability'] - result1['probability'], 2)}%"
    else:
        verdict = "Both students have equal placement probability"

    return {
        "student1": result1,
        "student2": result2,
        "verdict":  verdict
    }

# Model Info
@app.get("/model/info")
def model_info():
    return {
        "model":    "Random Forest Classifier",
        "features": features,
        "total_features": len(features)
    }