from core.dispersion_backend import (ellipse_math, haversine_nm)

from datetime import datetime
import joblib
import pandas as pd

def run_predictions(forecast_data):
	forecast_dataframe = to_dataframe(forecast_data)
	parameters_forecast_dataframe = forecast_dataframe.drop(columns=["id", "fetched_time", "forecast_hour"])

	model_names = ["model_main_distance", "model_main_latitude", "model_main_longitude",
        "model_drogue_distance", "model_drogue_latitude", "model_drogue_longitude",
        "model_ballistic_distance", "model_ballistic_latitude","model_ballistic_longitude"
	]

	loaded_models= {}

	for name in model_names:
		model = joblib.load(f"ml_models/{name}.joblib")
		loaded_models[name] = model
	
	results = {
		"standard" : {},
		"drogue_only" : {},
		"ballistic" : {}
	}

	# Each model will return a COLUMN as a list
	for name, model in loaded_models.items():
        # Ensure that all the columns are in the same order as the model trained!
		feature_columns = model.get_booster().feature_names
		column = model.predict(parameters_forecast_dataframe[feature_columns])
		results[get_deployment_type(name)][get_target_column(name)] = column
        
	return forecast_dataframe[["id", "forecast_hour"]], results 

def get_target_column(model_name: str) -> str:
    if model_name.endswith("_distance"):
        return "predicted_dist_nm"
    elif model_name.endswith("_latitude"):
        return "landing_lat"
    elif model_name.endswith("_longitude"):
        return "landing_lon"

    raise ValueError(f"Unknown model: {model_name}")

def get_deployment_type(model_name: str) -> str:
    if model_name.startswith("model_main_"):
        return "standard"
    elif model_name.startswith("model_drogue_"):
        return "drogue_only"
    elif model_name.startswith("model_ballistic_"):
        return "ballistic"
    raise ValueError(f"Unknown model: {model_name}")

def to_dataframe(forecast_data):
	"""
	Forecast data starts as an object. Each index of the object represents a row. These must be converted to a python container first
	or else the dataframe will attempt to map to the object's data address. Format below of print(forecast_data[0]):

	<Forecasts (id=1, ... , pressure = 12 ...)>
	"""

	data = []
	for row in forecast_data:
		# .__dict__.copy() used to create a shallow copy of an object's attribute namespace dictionary
		row_dict = row.__dict__.copy()
		row_dict.pop('_sa_instance_state', None)  # Drops SQLAlchemy internal tracker
		data.append(row_dict)

	# Load into pandas dataframe
	forecast_dataframe = pd.DataFrame(data)
	return forecast_dataframe