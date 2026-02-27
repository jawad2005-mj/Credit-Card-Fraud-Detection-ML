import pandas as pd
import os
import kagglehub

# 1. Download Data
print("⏳ Downloading dataset...")
path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")
csv_path = os.path.join(path, "creditcard.csv")

# 2. Load Data
df = pd.read_csv(csv_path)

# 3. Create Sample (WITHOUT manual scaling)
# We take raw data because the Pipeline inside the Model will handle scaling
print("⚙️ Generating raw sample...")
final_df = df.sample(n=500, random_state=42)

# Drop the Class column (removing the answer sheet)
if 'Class' in final_df.columns:
    final_df = final_df.drop('Class', axis=1)

# 4. Save
final_df.to_csv("test_transactions.csv", index=False)
print("✅ Done! 'test_transactions.csv' saved with RAW data.")