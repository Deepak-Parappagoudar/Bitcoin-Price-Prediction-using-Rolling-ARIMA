import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import pickle

# Read the CSV file
df = pd.read_csv('bitcoin_daily_historical.csv', index_col='Date', parse_dates=True)
df.drop('Currency', axis=1, inplace=True)

# Filter the DataFrame for dates after 2016-12-31 (since there wan't much fluctuations before this point)
df = df[df.index > '2016-12-31']

index = int(len(df) * 0.85)

df_train = df.iloc[:index]
df_test = df.iloc[index:]

train_data = df_train['Price(USD)'].values.tolist()
test_data = df_test['Price(USD)'].values.tolist()

model_predictions = []
num_test = len(test_data)

# We append each value of the test data to the training data, before re-fitting the model with the updated data (& hence Rolling-ARIMA). 
for i in range(num_test):
    model = ARIMA(train_data, order=(1, 1, 1))
    model_fit = model.fit()
    output = model_fit.forecast()
    model_predictions.append(output[0])
    actual_price_test = test_data[i]
    train_data.append(actual_price_test)

# Save the ARIMA model
with open('arima_model.pkl', 'wb') as file:
    pickle.dump(model_fit, file)
