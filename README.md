# 🎓 Student Placement Prediction System

A full-stack Machine Learning web application that predicts whether a student 
will get placed based on their academic performance, skills, and activities.

**Features:**
- ⚡ **Two UI Options**: Use Streamlit for quick analysis or React for a modern web experience
- 🔮 **Single Predictions**: Predict placement probability for individual students
- 📂 **Batch Processing**: Upload CSV files for bulk predictions
- 🆚 **Student Comparison**: Compare multiple students to identify strengths/weaknesses
- 📊 **Model Insights**: View feature importance and model performance metrics
- 🤖 **Machine Learning**: Random Forest classifier with 92% accuracy

---

## 📌 Project Overview

This system helps colleges and placement cells to:
- Predict placement probability of a student
- Identify at-risk students before placements
- Understand which factors affect placement the most

---

## 🎯 Problem Statement

Build a placement prediction system that:
- Takes student academic and skill data as input
- Predicts Placed / Not Placed with probability
- Flags at-risk students for early intervention

---

## 🏗️ Project Structure
```
placement_prediction/
│
├── data/                        ← datasets
│   ├── Placement_Data_Full_Class.csv
│   ├── placement_data.csv
│   └── sample_students.csv
│
├── model/                       ← trained model artifacts
│   ├── placement_model.pkl      ← trained Random Forest model
│   ├── scaler.pkl               ← standard scaler
│   ├── le_branch.pkl            ← branch encoder
│   ├── le_gender.pkl            ← gender encoder
│   ├── features.pkl             ← feature list
│   ├── feature_importance.png   ← feature importance chart
│   └── confusion_matrix.png     ← confusion matrix
│
├── backend/                     ← FastAPI REST API
│   ├── main.py                  ← FastAPI server with endpoints
│   ├── utils.py                 ← backend utilities
│   └── __pycache__/
│
├── frontend/                    ← React + Vite web application
│   ├── src/
│   │   ├── main.jsx             ← React entry point
│   │   ├── App.jsx              ← main component
│   │   ├── index.css            ← global styles
│   │   └── components/
│   │       ├── Navbar.jsx       ← navigation component
│   │       ├── SinglePrediction.jsx    ← single student prediction
│   │       ├── BulkPrediction.jsx      ← batch CSV upload
│   │       ├── Comparison.jsx          ← student comparison
│   │       └── ModelInsights.jsx       ← model visualizations
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── eslint.config.js
│
├── training/
│   └── train_model.py           ← model training script
│
├── app.py                       ← Streamlit web application (alternative UI)
├── utils.py                     ← shared utility functions
├── requirements.txt             ← Python dependencies
└── README.md                    ← project documentation
```

---

## 🧠 ML Models Used

| Model | Purpose |
|---|---|
| Random Forest Classifier | Main prediction model |
| Logistic Regression | Baseline comparison model |

---

## 📊 Features Used

### Academic
- SSC Percentage
- HSC Percentage
- Degree Percentage
- CGPA
- Active Backlogs

### Skills
- Aptitude Test Score
- Coding Test Score
- Technical Interview Score
- Communication Score

### Activities
- Internships Count
- Projects Count
- Certifications Count
- Hackathons Participated
- Work Experience (months)

### Engagement
- Attendance Percentage
- Extracurricular Participation

### Derived Features
- Academic Score = 0.3×SSC + 0.3×HSC + 0.4×Degree
- Skill Score = Average of all skill scores
- Activity Score = Sum of all activity counts

---

## 🚦 Risk Classification

| Probability | Risk Level |
|---|---|
| Above 60% | 🟢 Low Risk |
| 40% to 60% | 🟡 Medium Risk |
| Below 40% | 🔴 High Risk |

---

## 🏗️ Tech Stack

### Backend & Core
| Component | Technology |
|---|---|
| Language | Python 3.13 |
| ML Library | Scikit-learn |
| API Framework | FastAPI |
| Data Handling | Pandas, NumPy |
| Model Storage | Joblib |

### Frontend Options
| Option | Technology |
|---|---|
| **React Frontend** | React 18 + Vite + JSX |
| **Alternative UI** | Streamlit |
| **Styling** | CSS with custom properties |

### Development & DevOps
| Component | Technology |
|---|---|
| Visualization | Matplotlib, Seaborn |
| Frontend Build Tool | Vite |
| Linting | ESLint |
| Version Control | Git + GitHub |

---

## ⚙️ How to Run

### 📋 Prerequisites
- Python 3.13+
- Node.js 16+ (for React frontend)
- Git

### 🚀 Quick Start: Streamlit Application

#### Step 1 — Clone the repository
```bash
git clone https://github.com/tanmaysurushe2005/placement-prediction-system.git
cd placement-prediction-system
```

#### Step 2 — Install Python dependencies
```bash
pip install -r requirements.txt
```

#### Step 3 — Train the model (if needed)
```bash
cd training
python train_model.py
cd ..
```

#### Step 4 — Run the Streamlit app
```bash
streamlit run app.py
```
The app will start and display:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

#### Step 5 — Access the app
Open your browser and navigate to:
```
http://localhost:8501
```

**Available Tabs:**
- 🔮 **Single Prediction** - Predict placement for one student
- 📂 **Bulk Prediction** - Upload CSV for batch predictions
- 🆚 **Comparison** - Compare multiple students
- 📊 **Model Insights** - View feature importance & metrics

---

### 🎨 Full Stack: React Frontend + FastAPI Backend

#### Step 1 — Clone & navigate to project
```bash
git clone https://github.com/tanmaysurushe2005/placement-prediction-system.git
cd placement-prediction-system
```

#### Step 2 — Setup Python backend
```bash
# Install Python dependencies
pip install -r requirements.txt

# Train the model (if needed)
cd training
python train_model.py
cd ..

# Start FastAPI server
cd backend
python -m uvicorn main:app --reload
# API runs on http://localhost:8000
cd ..
```

#### Step 3 — Setup React frontend
```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
# App runs on http://localhost:5173
```

#### Step 4 — Access the application
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

---

### 🎛️ Backend API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/predict` | POST | Single student prediction |
| `/batch-predict` | POST | Batch predictions from CSV |
| `/compare` | POST | Compare multiple students |
| `/model-insights` | GET | Feature importance & metrics |

---

### 🔌 React Frontend Components

| Component | Feature |
|---|---|
| **Navbar** | Navigation between pages |
| **SinglePrediction** | Predict placement for one student |
| **BulkPrediction** | Upload CSV for batch predictions |
| **Comparison** | Compare 2+ students side-by-side |
| **ModelInsights** | Visualize feature importance & confusion matrix |

---

## 📈 Model Performance

| Model | Accuracy |
|---|---|
| Logistic Regression | ~85% |
| Random Forest | ~92% |

---

## 🔮 Future Scope

- Company specific placement prediction
- Real college database integration
- Student batch comparison dashboard
- Email alerts for at-risk students
- Mobile application version

---

## ⚠️ Limitations

- Currently uses synthetic dataset
- Company wise prediction not implemented
- Needs real college data for production use

---

## 👨‍💻 Developer

**Tanmay Surushe**
Industry Sponsored Project — 2026

---

## 📄 License

This project is for educational purposes only.