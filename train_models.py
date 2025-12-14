import pandas as pd
import numpy as np
import pickle
import os
import shap
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split

# Ensure artifacts directory
ARTIFACTS_DIR = 'ml_artifacts'
if not os.path.exists(ARTIFACTS_DIR):
    os.makedirs(ARTIFACTS_DIR)

def generate_synthetic_data(n=1000):
    np.random.seed(42)
    data = pd.DataFrame()
    data['income'] = np.random.normal(60000, 20000, n)
    data['amount_requested'] = np.random.normal(20000, 10000, n)
    data['credit_score'] = np.random.normal(700, 50, n)
    data['debt'] = np.random.normal(10000, 5000, n)
    data['term_months'] = np.random.choice([12, 24, 36, 48, 60], n)
    
    # Clip values to realistic ranges
    data['income'] = data['income'].clip(20000, 200000)
    data['credit_score'] = data['credit_score'].clip(300, 850)
    data['amount_requested'] = data['amount_requested'].clip(1000, 100000)
    data['debt'] = data['debt'].clip(0, 100000)
    
    # Feature Engineering for Target
    data['dti'] = data['debt'] / (data['income'] / 12)
    data['payment_ratio'] = (data['amount_requested'] / data['term_months']) / (data['income'] / 12)
    
    # Define Target: Default (Risk)
    # Higher DTI, Lower Credit Score, Higher Payment Ratio -> Higher Risk
    risk_score = (data['dti'] * 0.5) + (data['payment_ratio'] * 20) - ((data['credit_score'] - 600) / 100)
    risk_prob = 1 / (1 + np.exp(-risk_score)) # Sigmoid to probability
    data['defaulted'] = (np.random.random(n) < risk_prob).astype(int)
    
    # Define Target: Suggested Amount (Conservative)
    # Based on what they can afford (e.g., max 40% DTI including new loan)
    max_monthly = (data['income'] / 12) * 0.4
    available_monthly = max_monthly - (data['debt'] / 12) # Approximation
    data['suggested_amount'] = available_monthly * data['term_months'] * 0.9 # 90% conservative
    data['suggested_amount'] = data['suggested_amount'].clip(1000, 100000)

    return data

def train():
    print("Generating synthetic data...")
    df = generate_synthetic_data(2000)
    
    features = ['income', 'amount_requested', 'credit_score', 'debt', 'term_months']
    X = df[features]
    y_risk = df['defaulted']
    y_amount = df['suggested_amount']
    
    print("Training Risk Classifier...")
    risk_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    risk_model.fit(X, y_risk)
    
    print("Training Amount Regressor...")
    amount_model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    amount_model.fit(X, y_amount)
    
    print("Generating SHAP Explainer...")
    # Use TreeExplainer for fast/exact values
    explainer = shap.TreeExplainer(risk_model)
    
    # Save artifacts
    print(f"Saving artifacts to {ARTIFACTS_DIR}...")
    with open(os.path.join(ARTIFACTS_DIR, 'model_risk.pkl'), 'wb') as f:
        pickle.dump(risk_model, f)
        
    with open(os.path.join(ARTIFACTS_DIR, 'model_amount.pkl'), 'wb') as f:
        pickle.dump(amount_model, f)
        
    with open(os.path.join(ARTIFACTS_DIR, 'explainer.pkl'), 'wb') as f:
        pickle.dump(explainer, f)
        
    print("Training complete.")

if __name__ == '__main__':
    train()
