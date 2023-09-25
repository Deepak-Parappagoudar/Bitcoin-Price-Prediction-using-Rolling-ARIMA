import pandas as pd
import requests

def get_new_prices(historical_data):
    """
    Parameters
    ----------
    historical_data : DataFrame
        DataFrame read from a CSV containing all the historical prices by day.

    Returns
    -------
    None
        Finds the discrepancy in days between the CSV file and data from the API
        and uses get_historical_prices to append the new data to the existing CSV.

    """

    # Need a try statement as if the CSV is open with Excel, it may reorder the dates.
    try:
        historical_data['Date'] = pd.to_datetime(historical_data['Date'], format='%Y/%m/%d')
    except ValueError:
        historical_data['Date'] = pd.to_datetime(historical_data['Date'], format='%d/%m/%Y')

    max_date = historical_data['Date'].max()
    today_date = pd.to_datetime("today")
    date_difference = (today_date - max_date).days

    if date_difference > 0:
        chosen_currency = historical_data['Currency'][0]
        get_historical_prices(chosen_currency, date_difference, False)
    else:
        return

def get_historical_prices(chosen_currency, num_days, first_parse):
    """
    Parameters
    ----------
    chosen_currency : str
        Provide a valid crypto currency, e.g., 'bitcoin'.
    num_days : int
        Enter the number of days of history wanted.
    first_parse : bool
        True if it's the first time parsing, False otherwise.

    Returns
    -------
    None

    """

    response = requests.get(f'https://api.coingecko.com/api/v3/coins/{chosen_currency}/market_chart?vs_currency=usd&days={num_days}&interval=daily')
    hist_dict = response.json()

    data = pd.DataFrame.from_dict(hist_dict['prices'])
    data.rename(columns={0: 'Date', 1: 'Price(USD)'}, inplace=True)
    data['Date'] = pd.to_datetime(data['Date'], unit='ms')
    data['Date'] = data['Date'].dt.date
    data['Currency'] = chosen_currency

    if first_parse is False:
        data.to_csv(f'{chosen_currency}_daily_historical.csv', mode='a', header=False, index=False)
    else:
        data.to_csv(f'{chosen_currency}_daily_historical.csv', index=False)

chosen_currency = 'bitcoin'

try:
    historical_data = pd.read_csv(f'{chosen_currency}_daily_historical.csv')
except FileNotFoundError:
    historical_data = pd.DataFrame()

if len(historical_data) > 0:
    get_new_prices(historical_data)
else:
    get_historical_prices(chosen_currency, 3650, True)
