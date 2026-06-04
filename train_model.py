import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load and prepare data
df = pd.read_csv('data.csv')
if 'Unnamed: 32' in df.columns:
    df = df.drop('Unnamed: 32', axis=1)
if 'id' in df.columns:
    df = df.drop('id', axis=1)

df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
X = df.drop('diagnosis', axis=1)
y = df['diagnosis']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Impute and Scale
imputer = SimpleImputer(strategy='median')
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_imputed)
X_test_scaled = scaler.transform(X_test_imputed)

# Train VotingClassifier
print("Training SVM...")
svm_best = SVC(C=10, gamma=0.01, kernel='rbf', probability=True, random_state=42)
print("Training XGBoost...")
xgb_best = XGBClassifier(n_estimators=500, max_depth=3, learning_rate=0.01, subsample=0.9, colsample_bytree=0.9, eval_metric='logloss', use_label_encoder=False, random_state=42)
print("Training Logistic Regression...")
lr_best = LogisticRegression(C=1, max_iter=1000)

print("Creating Voting Classifier...")
voting = VotingClassifier(
    estimators=[('svm', svm_best), ('xgb', xgb_best), ('lr', lr_best)],
    voting='soft'
)

print("Fitting Voting Classifier...")
voting.fit(X_train_scaled, y_train)
y_pred_voting = voting.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred_voting)

# Save model
print("Saving model and scaler...")
joblib.dump(voting, 'final_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print(f'✓ Model trained and saved')
print(f'✓ Accuracy: {acc:.4f}')
