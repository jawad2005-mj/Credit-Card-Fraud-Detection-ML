# 🛡️ FraudGuard AI: Real-Time Financial Fraud Detection System
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Machine Learning](https://img.shields.io/badge/Model-Random%20Forest-orange?style=for-the-badge)
![Backend](https://img.shields.io/badge/Backend-FastAPI-005571?style=for-the-badge&logo=fastapi)
![Frontend](https://img.shields.io/badge/UI-CustomTkinter-blueviolet?style=for-the-badge)

> **An enterprise-grade Machine Learning pipeline designed to identify fraudulent transactions in highly imbalanced financial datasets.**

---

## 📖 Executive Summary
**FraudGuard AI** is a full-stack, end-to-end Machine Learning solution. Unlike standard experimental notebooks, this project is engineered for **production deployment**. It tackles the critical challenge of credit card fraud (where only 0.17% of transactions are actually fraud) using advanced data augmentation (SMOTE) and robust feature scaling.

The system features a **Training Pipeline**, a **REST API** for real-time integration, and an interactive **Dashboard** for non-technical stakeholders and fraud analysts.

---

## 🚀 Key Features
* **Advanced Predictive Modeling:** Utilizes a Random Forest Classifier trained on highly imbalanced data using SMOTE.
* **Production-Ready Pipeline:** Data scaling (`RobustScaler`) and model inference are wrapped into a single serialized pipeline (`fraud_pipeline.pkl`).
* **Real-Time REST API:** Built with FastAPI to handle both single transaction scoring and bulk batch processing.
* **Interactive Enterprise Dashboard:** A sleek, dark-themed UI built with CustomTkinter for visualizing fraud predictions directly from CSV uploads.

---

## 📂 Repository Structure

| File | Description |
|------|-------------|
| `logistic_model_advanced.py` | The main training script handling data downloading, SMOTE balancing, pipeline creation, and model serialization. |
| `fraud_pipeline.pkl` | The exported Machine Learning pipeline (Scaler + Random Forest Model). |
| `fraud_api.py` | FastAPI backend application serving predictions via REST endpoints. |
| `fraud_detection_dashboard.py`| The frontend GUI application for business analysts to upload transactions and view results. |
| `smart_sample.py` | Script to fetch and generate realistic testing data (`test_transactions.csv`). |
| `credit_card_fraud_detection.ipynb`| Jupyter Notebook containing initial Exploratory Data Analysis (EDA) and model experimentation. |
| `test_transactions.csv` | Sample batch dataset to test the API and Dashboard. |

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/FraudGuard-AI.git
cd FraudGuard-AI
```

### 2. Install Dependencies
```bash
pip install pandas scikit-learn imbalanced-learn fastapi uvicorn customtkinter matplotlib joblib kagglehub
```

### 3. Generate the Model & Test Data (Optional if .pkl is provided)
```bash
python logistic_model_advanced.py
python smart_sample.py
```

---

## 💻 How to Run the System

### Option A: Run the Analyst Dashboard (GUI)
Simply execute the dashboard script. A graphical interface will open allowing you to upload the test_transactions.csv file and visualize the fraud analysis.

```bash
python fraud_detection_dashboard.py
```

### Option B: Run the FastAPI Server (Backend)
Start the API server to allow external applications to make predictions.

```bash
uvicorn fraud_api:app --reload
```

Once running, you can test the API directly via the Swagger UI at: http://127.0.0.1:8000/docs

---

## 📊 Business Impact
By deploying this model, financial institutions can automatically flag high-risk transactions in milliseconds, significantly reducing chargeback losses and manual review overhead while maintaining a low false-positive rate.

---

## 👨‍💻 Author

**Muhammad Jawad**

**Role:** ML Developer & Data Analyst

**LinkedIn:** https://www.linkedin.com/in/muhammad-jawad-92380629a/


