import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# ─────────────────────────────────────────
# STEP 1 — Generate Synthetic Dataset
# ─────────────────────────────────────────
np.random.seed(42)
n = 500

branches = ['CSE', 'IT', 'ECE', 'Mechanical', 'Civil']
genders = ['Male', 'Female']

data = {
    'ssc_percentage':             np.random.uniform(50, 98, n),
    'hsc_percentage':             np.random.uniform(50, 98, n),
    'degree_percentage':          np.random.uniform(50, 98, n),
    'cgpa':                       np.random.uniform(5.0, 10.0, n),
    'active_backlogs':            np.random.randint(0, 5, n),
    'aptitude_test_score':        np.random.uniform(30, 100, n),
    'coding_test_score':          np.random.uniform(20, 100, n),
    'technical_interview_score':  np.random.uniform(20, 100, n),
    'communication_score':        np.random.uniform(20, 100, n),
    'internships_count':          np.random.randint(0, 4, n),
    'projects_count':             np.random.randint(0, 6, n),
    'certifications_count':       np.random.randint(0, 5, n),
    'hackathons_participated':    np.random.randint(0, 5, n),
    'attendance_percentage':      np.random.uniform(50, 100, n),
    'extracurricular_participation': np.random.randint(0, 2, n),
    'work_experience_months':     np.random.randint(0, 12, n),
    'branch':                     np.random.choice(branches, n),
    'gender':                     np.random.choice(genders, n),
}

df = pd.DataFrame(data)

# ─────────────────────────────────────────
# STEP 2 — Create Derived Features
# ─────────────────────────────────────────
df['academic_score'] = (
    0.3 * df['ssc_percentage'] +
    0.3 * df['hsc_percentage'] +
    0.4 * df['degree_percentage']
)

df['skill_score'] = (
    df['aptitude_test_score'] +
    df['coding_test_score'] +
    df['technical_interview_score'] +
    df['communication_score']
) / 4

df['activity_score'] = (
    df['internships_count'] +
    df['projects_count'] +
    df['certifications_count'] +
    df['hackathons_participated']
)

# ─────────────────────────────────────────
# STEP 3 — Generate Target Variable
# ─────────────────────────────────────────
placement_score = (
    df['cgpa'] * 5 +
    df['skill_score'] * 0.3 +
    df['activity_score'] * 2 +
    df['attendance_percentage'] * 0.1 -
    df['active_backlogs'] * 3
)

threshold = placement_score.median()
df['placed'] = (placement_score >= threshold).astype(int)

# ─────────────────────────────────────────
# STEP 4 — Save Dataset
# ─────────────────────────────────────────
os.makedirs('../data', exist_ok=True)
df.to_csv('../data/placement_data.csv', index=False)
print("✅ Dataset saved to data/placement_data.csv")
print(f"   Total records : {len(df)}")
print(f"   Placed        : {df['placed'].sum()}")
print(f"   Not Placed    : {len(df) - df['placed'].sum()}")

# ─────────────────────────────────────────
# STEP 5 — Preprocessing
# ─────────────────────────────────────────
le_branch = LabelEncoder()
le_gender = LabelEncoder()

df['branch']  = le_branch.fit_transform(df['branch'])
df['gender']  = le_gender.fit_transform(df['gender'])

features = [
    'ssc_percentage', 'hsc_percentage', 'degree_percentage', 'cgpa',
    'active_backlogs', 'aptitude_test_score', 'coding_test_score',
    'technical_interview_score', 'communication_score',
    'internships_count', 'projects_count', 'certifications_count',
    'hackathons_participated', 'attendance_percentage',
    'extracurricular_participation', 'work_experience_months',
    'branch', 'gender',
    'academic_score', 'skill_score', 'activity_score'
]

X = df[features]
y = df['placed']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale for Logistic Regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ─────────────────────────────────────────
# STEP 6 — Train Models
# ─────────────────────────────────────────

# Logistic Regression
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train_scaled, y_train)
lr_pred = lr.predict(X_test_scaled)
lr_acc  = accuracy_score(y_test, lr_pred)

print(f"\n📊 Logistic Regression Accuracy : {lr_acc * 100:.2f}%")
print(classification_report(y_test, lr_pred))

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc  = accuracy_score(y_test, rf_pred)

print(f"🌲 Random Forest Accuracy       : {rf_acc * 100:.2f}%")
print(classification_report(y_test, rf_pred))

# ─────────────────────────────────────────
# STEP 7 — Save Best Model
# ─────────────────────────────────────────
os.makedirs('../model', exist_ok=True)

joblib.dump(rf,     '../model/placement_model.pkl')
joblib.dump(scaler, '../model/scaler.pkl')
joblib.dump(le_branch, '../model/le_branch.pkl')
joblib.dump(le_gender, '../model/le_gender.pkl')
joblib.dump(features,  '../model/features.pkl')

print("\n✅ Model saved to model/placement_model.pkl")

# ─────────────────────────────────────────
# STEP 8 — Feature Importance Plot
# ─────────────────────────────────────────
importance_df = pd.DataFrame({
    'Feature':   features,
    'Importance': rf.feature_importances_
}).sort_values('Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
plt.title('Feature Importance - Random Forest')
plt.tight_layout()
plt.savefig('../model/feature_importance.png')
plt.show()
print("✅ Feature importance plot saved to model/feature_importance.png")

# ─────────────────────────────────────────
# STEP 9 — Confusion Matrix
# ─────────────────────────────────────────
cm = confusion_matrix(y_test, rf_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Not Placed', 'Placed'],
            yticklabels=['Not Placed', 'Placed'])
plt.title('Confusion Matrix - Random Forest')
plt.tight_layout()
plt.savefig('../model/confusion_matrix.png')
plt.show()
print("✅ Confusion matrix saved to model/confusion_matrix.png")

print("\n🎉 Training complete! All files saved in /model folder.")