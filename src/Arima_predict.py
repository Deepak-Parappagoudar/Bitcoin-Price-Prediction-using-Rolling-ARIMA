import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import pickle
from datetime import date



import os

# Get the directory where the current script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the script's directory
os.chdir(script_directory)

with open('arima_model.pkl', 'rb') as file:
    model_fit= pickle.load(file)



# Read the CSV file
df = pd.read_csv('bitcoin_daily_historical.csv', index_col='Date', parse_dates=True)
df.drop('Currency', axis=1, inplace=True)

# User enters a date for prediction
user_input_date = input("Enter a date for prediction (YYYY-MM-DD): ")
user_input_date = pd.to_datetime(user_input_date)

# Calculate the number of steps ahead to predict

today = date.today()
today=pd.to_datetime(today)
num_steps_ahead = (user_input_date - today).days
# start_ind=len(df)
# end_ind=len(df)+num_steps_ahead
prediction = model_fit.forecast(steps=num_steps_ahead)
# prediction = forecast.predicted_mean[0]
# # Print the prediction
print("Predicted Price for", user_input_date.strftime('%Y-%m-%d'), ": $", prediction)


# # $ 27208.537129446442
