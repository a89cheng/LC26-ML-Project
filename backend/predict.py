from core.dispersion_backend import (ellipse_math, haversine_nm)

def run_dispersion(forecast_row):
    pass




"""
         - check class balance: how many within vs outside 10 NM

Step 4   Engineer features
         - select the 38 wind columns as X (speeds + directions at 19 altitudes)
         - set within_safe_zone as y (your target label)

Step 5   Split data
         - use train_test_split from sklearn with test_size=0.2

Step 6   Train XGBoost classifier
         - fit on training data

Step 7   Evaluate
         - compute AUC-ROC score on test data
         - plot feature importances

Step 8   Save the model
         - use joblib.dump() into backend/ml/model.joblib

Step 9   Create backend/ml/features.py
         - write a function that takes a forecast dataframe row
           and returns a feature vector matching what the model was trained on

Step 10  Create backend/predict.py
         - load the model with joblib.load()
         - write run_prediction(forecast_row) that calls features.py
           and returns p_safe_launch and top_risk_altitude
"""