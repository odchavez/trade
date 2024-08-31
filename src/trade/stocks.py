import yfinance as yf
from datetime import datetime, timedelta


class STOCKS:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_historical_returns(self, interval=5, start="2000-01-01", end="2024-12-31"):

        stock_data = yf.download(self.ticker, start=start, end=end)
        #stock_data['Return'] = stock_data['Adj Close'].pct_change()

        stock_data[f'{interval}-Day Return'] = stock_data['Adj Close'].pct_change(periods=-interval)
        stock_data[f'Max High {interval}-Day'] = stock_data['High'].rolling(window=interval).max().shift(-interval+1)
        stock_data[f'{interval}-Day Max High Return'] = (stock_data[f'Max High {interval}-Day'] - stock_data['Open']) / stock_data['Open']

        stock_data[f'Min Low {interval}-Day'] = stock_data['Low'].rolling(window=interval).min().shift(-interval+1)
        stock_data[f'{interval}-Day Min Low Return'] = (stock_data[f'Min Low {interval}-Day'] - stock_data['Open']) / stock_data['Open']
        stock_data.dropna(inplace=True)

        return stock_data 
    
    def days_until(self, date_str):
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        current_date = datetime.today()
        difference_in_days = (target_date - current_date).days
        return difference_in_days