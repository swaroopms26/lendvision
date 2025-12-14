from app import create_app, db
from app.models import LoanApplication
import json

app = create_app()

with app.app_context():
    application = LoanApplication.query.get(1)
    if application:
        print(f"Application ID: {application.id}")
        shap_json = application.ml_shap_values
        print(f"Raw SHAP JSON: {shap_json}")
        
        shap_dict = application.get_shap()
        print(f"Parsed SHAP Dict: {shap_dict}")
        
        for k, v in shap_dict.items():
            print(f"Key: {k}, Value: {v}, Type: {type(v)}")
    else:
        print("Application 1 not found")
