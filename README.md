# 🩺 Heart Disease Prediction and Monitoring System

An AI-powered web application for predicting and monitoring heart disease using a **hybrid Transformer–CNN deep learning model**.  
The system allows **patients**, **clinicians**, and **administrators** to interact securely — from uploading ECG data to generating interpretable risk reports with SHAP explanations.

---

## 🌟 Features

### 👩‍⚕️ For Patients
- Register, login, and upload ECG or clinical data.
- View prediction results (Yes/No) and confidence score.
- Download detailed PDF reports.
- Visualize trends of past health records with interactive charts.

### 🧑‍🔬 For Clinicians
- Access assigned patients’ data.
- Validate AI predictions and add clinical feedback.
- View explainability insights (SHAP plots, feature importance).
- Receive alerts for high-risk patients.

### 🛠️ For Admin (IT Staff)
- Manage users and roles.
- Monitor data compliance and logs.
- Oversee model updates and dataset integration.

---

## 🧠 AI & Model Overview

- **Model Architecture:** Hybrid Transformer–CNN  
- **Data Sources:** Kaggle clinical datasets + hospital ECG data  
- **Explainability:** SHAP-based feature attribution  
- **Visualization:** Plotly for trend and interpretability charts  

---

## ⚙️ System Architecture

**Layers:**
1. **Presentation Layer:** Django web UI (or React frontend)  
2. **Application Layer:** Django backend + REST APIs  
3. **Data Layer:** PostgreSQL database for patients, ECGs, and predictions  
4. **Model Layer:** Transformer–CNN deep learning model served via Django or FastAPI microservice  
5. **Integration Layer:** API gateway for communication and deployment (Docker/Cloud)

---

## 🚀 Getting Started

### 🧩 Prerequisites
- Python 3.11+
- PostgreSQL
- pip / virtualenv
- Git

### ⚡ Installation

```bash
# Clone the repository
git clone https://github.com/iamExony/heart-disease-ai.git
cd heart-disease-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
