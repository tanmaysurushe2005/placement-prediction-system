# 🎓 Student Placement Prediction System

A Machine Learning based web application that predicts whether a student 
will get placed based on their academic performance, skills, and activities.

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
├── data/
│   └── placement_data.csv       ← dataset
│
├── model/
│   ├── placement_model.pkl      ← trained Random Forest model
│   ├── scaler.pkl               ← standard scaler
│   ├── le_branch.pkl            ← branch encoder
│   ├── le_gender.pkl            ← gender encoder
│   ├── features.pkl             ← feature list
│   ├── feature_importance.png   ← feature importance chart
│   └── confusion_matrix.png     ← confusion matrix
│
├── training/
│   └── train_model.py           ← model training script
│
├── app.py                       ← Streamlit web application
├── utils.py                     ← helper functions
├── requirements.txt             ← dependencies
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

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| ML Library | Scikit-learn |
| UI Framework | Streamlit |
| Data Handling | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Model Storage | Joblib |
| Version Control | Git + GitHub |

---

## ⚙️ How to Run

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/placement-prediction-system.git
cd placement-prediction-system
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Train the model
```bash
cd training
python train_model.py
cd ..
```

### Step 4 — Run the app
```bash
streamlit run app.py
```

### Step 5 — Open in browser
```
http://localhost:8501
```

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