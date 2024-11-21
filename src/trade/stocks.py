import yfinance as yf
from datetime import datetime, timedelta


class Stocks:
    def __init__(self, ticker, start="2000-01-01", end="2024-12-31"):
        self.ticker = ticker
        self.stock_data = yf.download(self.ticker, start=start, end=end)

    def get_historical_returns(self, interval=5):

        
        #stock_data['Return'] = stock_data['Adj Close'].pct_change()

        self.stock_data[f'{interval}-Day Return'] = self.stock_data['Adj Close'].pct_change(periods=-interval)
        self.stock_data[f'Max High {interval}-Day'] = self.stock_data['High'].rolling(window=interval).max().shift(-interval+1)
        self.stock_data[f'{interval}-Day Max High Return'] = (self.stock_data[f'Max High {interval}-Day'] - self.stock_data['Open']) / self.stock_data['Open']

        self.stock_data[f'Min Low {interval}-Day'] = self.stock_data['Low'].rolling(window=interval).min().shift(-interval+1)
        self.stock_data[f'{interval}-Day Min Low Return'] = (self.stock_data[f'Min Low {interval}-Day'] - self.stock_data['Open']) / self.stock_data['Open']
        self.stock_data.dropna(inplace=True)

        return self.stock_data 
    
    def days_until(self, date_str):
        target_date = datetime.strptime(date_str, '%Y-%m-%d')
        current_date = datetime.today()
        difference_in_days = (target_date - current_date).days
        return difference_in_days
    
    def get_current_stock_price(self):
        """
        Get the current stock price for the given ticker.
        """
        stock = yf.Ticker(self.ticker)
        history = stock.history(period="3mo")
        current_price = history["Close"].iloc[-1]
        sma_10 = history["Close"].tail(10).mean()
        sma_50 = history["Close"].tail(50).mean()
        return current_price, sma_10, sma_50