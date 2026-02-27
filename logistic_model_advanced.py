import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
import joblib
import kagglehub
import os

print("⏳ Downloading Data & Training Model... (Thoda wait karein)")

# 1. Load Data
try:
    path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
    csv_path = os.path.join(path, "creditcard.csv")
    df = pd.read_csv(csv_path)
except Exception as e:
    print(f"❌ Error downloading data: {e}")
    exit()

# 2. Prepare Data
X = df.drop('Class', axis=1)
y = df['Class']

# 3. SMOTE (Balancing)
print("⚖️ Balancing Data (SMOTE)...")
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# 4. Create Pipeline
pipeline = Pipeline([
    ('scaler', RobustScaler()), 
    ('model', RandomForestClassifier(n_estimators=20, max_depth=10, random_state=42, n_jobs=-1))
])

# 5. Train
print("⚙️ Training Model on Balanced Data...")
pipeline.fit(X_resampled, y_resampled)

# 6. Save
joblib.dump(pipeline, 'fraud_pipeline.pkl')
print("✅ SUCCESS! 'fraud_pipeline.pkl' ban gayi hai.")
print("👉 Ab aap API dobara start kar sakte hain.")