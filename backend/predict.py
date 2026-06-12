from core.dispersion_backend import (ellipse_math, haversine_nm)

from datetime import datetime
import joblib
import pandas as pd

def run_predictions(forecast_data):
	forecast_dataframe = to_dataframe(forecast_data)

	model_names = ["model_main_distance", "model_main_latitude", "model_main_longitude",
        "model_drogue_distance", "model_drogue_latitude", "model_drogue_longitude",
        "model_ballistic_distance", "model_ballistic_latitude","model_ballistic_longitude"
	]

	loaded_models= {}

	for name in model_names:
		model = joblib.load(f"ml_models/{name}.joblib")
		loaded_models[name] = model
	
	# Name of model : [[prediction column] , [RMS, R^2], timestamp] 
	results = {}

	# Each model will return a COLUMN as a list
	for name, model in loaded_models.items():
		column = model.predict(forecast_dataframe)
		results[model] = [column, lookup_accuracy(name), datetime.now()] 

	return results 


def lookup_accuracy(model_name):
	rms_r2_values = {
		"model_main_distance": [0.5941581098089428, 0.8967763807664032],
		"model_main_latitude": [0.013362417368037857, 0.9639279651474006],
		"model_main_longitude": [0.012593585732728941, 0.9704828081076198],

		"model_drogue_distance": [0.26308866794816776, 0.9383076216292607],
		"model_drogue_latitude": [0.004852698418652511, 0.9313476615413283],
		"model_drogue_longitude": [0.007384831731377218, 0.9488180896969025],

		"model_ballistic_distance": [0.22841182059386442, 0.9760741175566592],
		"model_ballistic_latitude": [0.009483387312628664, 0.8413115300524789],
		"model_ballistic_longitude": [0.009040553192137498, 0.94463293187803],
	}
	return [rms_r2_values[model_name]]


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