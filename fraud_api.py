from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import io
from typing import List

# 1. API APP SETUP
app = FastAPI(
    title="🛡️ FraudGuard API",
    description="Professional API for Credit Card Fraud Detection (Single & Batch Processing)",
    version="2.0"
)

# 2. LOAD MODEL (Global Variable)
# Hum start mein hi model load kar lenge taake har request par time waste na ho
try:
    pipeline = joblib.load('fraud_pipeline.pkl')
    print("✅ Model Loaded Successfully!")
except Exception as e:
    print(f"⚠️ Error: Model file not found. Make sure 'fraud_pipeline.pkl' exists. {e}")
    pipeline = None

# 3. DEFINE INPUT SCHEMA (For Single Transaction)
# User ko 30 values ki list deni hogi (Time, V1-V28, Amount)
class TransactionInput(BaseModel):
    features: List[float] 
    # Example: [0.0, -1.3, 0.5, ... (30 values) ..., 100.50]

# --- HELPER FUNCTION ---
def get_column_names():
    # Model ko dataframe column names chahiye hote hain
    return ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']

# ==========================
# API ENDPOINTS
# ==========================

@app.get("/")
def home():
    return {"message": "FraudGuard API is Running. Go to /docs for testing."}

# 1. SINGLE TRANSACTION PREDICTION
@app.post("/predict_transaction")
def predict_single(data: TransactionInput):
    if pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    # Check if 30 values are provided
    if len(data.features) != 30:
        raise HTTPException(status_code=400, detail=f"Expected 30 feature values, got {len(data.features)}")

    # Convert list to DataFrame
    cols = get_column_names()
    df_input = pd.DataFrame([data.features], columns=cols)
    
    # Predict
    prediction = pipeline.predict(df_input)[0]
    probability = pipeline.predict_proba(df_input)[0][1] # Fraud hone ke % chance
    
    result = "FRAUD" if prediction == 1 else "Normal"
    risk_level = "High" if probability > 0.7 else ("Medium" if probability > 0.3 else "Low")

    return {
        "status": "success",
        "prediction": result,
        "fraud_probability": f"{probability:.2%}",
        "risk_level": risk_level
    }

# 2. BULK CSV FILE UPLOAD (Professional Feature)
@app.post("/upload_csv")
async def predict_bulk(file: UploadFile = File(...)):
    if pipeline is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    try:
        # Read uploaded file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Validate Columns (Check agar required columns hain)
        required_cols = get_column_names()
        # Agar file mein 'Class' column hai (jo answer hai), use hata do
        if 'Class' in df.columns:
            df = df.drop('Class', axis=1)
            
        # Ensure columns match standard format (Time, V1..V28, Amount)
        # Real scenario mein yahan strict checking hoti hai, hum assume kar rahe hain file sahi hai
        
        # Predict
        predictions = pipeline.predict(df)
        
        # Analysis
        total_tx = len(predictions)
        fraud_tx = sum(predictions == 1)
        
        return {
            "filename": file.filename,
            "total_transactions_scanned": total_tx,
            "fraud_detected": int(fraud_tx),
            "normal_transactions": int(total_tx - fraud_tx),
            "fraud_percentage": f"{(fraud_tx/total_tx)*100:.2f}%"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# SERVER RUNNER (Taa ke aap direct python file chala sakein)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)