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
# STEP 1 — Load Real Kaggle Dataset
# ─────────────────────────────────────────
df = pd.read_csv('../data/Placement_Data_Full_Class.csv')

print("✅ Real Kaggle dataset loaded")
print(f"   Shape : {df.shape}")
print(f"   Columns : {list(df.columns)}")

# ─────────────────────────────────────────
# STEP 2 — Drop Unnecessary Columns
# ─────────────────────────────────────────
df.drop(columns=['sl_no', 'ssc_b', 'hsc_b', 'hsc_s', 'degree_t'], inplace=True)

# ─────────────────────────────────────────
# STEP 3 — Rename Columns to Our Standard
# ─────────────────────────────────────────
df.rename(columns={
    'ssc_p':          'ssc_percentage',
    'hsc_p':          'hsc_percentage',
    'degree_p':       'degree_percentage',
    'etest_p':        'aptitude_test_score',
    'mba_p':          'communication_score',
    'workex':         'work_experience',
    'specialisation': 'branch',
    'status':         'placed'
}, inplace=True)

# ─────────────────────────────────────────
# STEP 4 — Fix Target Variable
# ─────────────────────────────────────────
df['placed'] = df['placed'].map({'Placed': 1, 'Not Placed': 0})

# ─────────────────────────────────────────
# STEP 5 — Fix Work Experience
# ─────────────────────────────────────────
df['work_experience_months'] = df['work_experience'].map({'Yes': 6, 'No': 0})
df.drop(columns=['work_experience'], inplace=True)

# ─────────────────────────────────────────
# STEP 6 — Add Missing Columns Synthetically
# ─────────────────────────────────────────
np.random.seed(42)
n = len(df)

df['cgpa']                        = df['degree_percentage'] / 10
df['active_backlogs']             = np.random.randint(0, 4, n)
df['coding_test_score']           = np.random.uniform(20, 100, n)
df['technical_interview_score']   = np.random.uniform(20, 100, n)
df['internships_count']           = np.random.randint(0, 4, n)
df['projects_count']              = np.random.randint(0, 6, n)
df['certifications_count']        = np.random.randint(0, 5, n)
df['hackathons_participated']     = np.random.randint(0, 5, n)
df['attendance_percentage']       = np.random.uniform(60, 100, n)
df['extracurricular_participation'] = np.random.randint(0, 2, n)

# ─────────────────────────────────────────
# STEP 7 — Handle Missing Values
# ─────────────────────────────────────────
# Fill ALL missing numeric columns with their mean
for col in df.select_dtypes(include=[np.number]).columns:
    df[col].fillna(df[col].mean(), inplace=True)

# Fill missing categorical columns with mode
for col in df.select_dtypes(include=['object']).columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# Drop any remaining nulls
df.dropna(inplace=True)

print(f"\n✅ After cleaning shape : {df.shape}")
print(f"   Placed     : {df['placed'].sum()}")
print(f"   Not Placed : {len(df) - df['placed'].sum()}")

# ─────────────────────────────────────────
# STEP 8 — Derived Features
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
# STEP 9 — Encode Categorical Columns
# ─────────────────────────────────────────
le_branch = LabelEncoder()
le_gender = LabelEncoder()

df['branch'] = le_branch.fit_transform(df['branch'])
df['gender'] = le_gender.fit_transform(df['gender'])

# ─────────────────────────────────────────
# STEP 10 — Prepare Features
# ─────────────────────────────────────────
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
# STEP 11 — Train Models
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
# STEP 12 — Save Everything
# ─────────────────────────────────────────
os.makedirs('../model', exist_ok=True)

joblib.dump(rf,        '../model/placement_model.pkl')
joblib.dump(scaler,    '../model/scaler.pkl')
joblib.dump(le_branch, '../model/le_branch.pkl')
joblib.dump(le_gender, '../model/le_gender.pkl')
joblib.dump(features,  '../model/features.pkl')

print("\n✅ Model saved to model/placement_model.pkl")

# ─────────────────────────────────────────
# STEP 13 — Feature Importance Plot
# ─────────────────────────────────────────
importance_df = pd.DataFrame({
    'Feature':    features,
    'Importance': rf.feature_importances_
}).sort_values('Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
plt.title('Feature Importance - Random Forest')
plt.tight_layout()
plt.savefig('../model/feature_importance.png')
plt.show()
print("✅ Feature importance plot saved")

# ─────────────────────────────────────────
# STEP 14 — Confusion Matrix
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
print("✅ Confusion matrix saved")

print("\n🎉 Training complete with real Kaggle data!")