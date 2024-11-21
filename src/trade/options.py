import yfinance as yf
from datetime import datetime, timedelta


class Options:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock_obj = yf.Ticker(self.ticker)

    def get_option_chains_within_cutoff_days(self, low_days_cutoff=0, high_days_cutoff=45):
        
        expirations = self.stock_obj.options
        low_cutoff_date = datetime.now() + timedelta(days=low_days_cutoff)
        high_cutoff_date = datetime.now() + timedelta(days=high_days_cutoff)
        def cutlow(fexp):
            return datetime.strptime(fexp, '%Y-%m-%d') >= low_cutoff_date
        def cuthigh(fexp):
            return datetime.strptime(fexp, '%Y-%m-%d') <= high_cutoff_date
        filtered_expirations = [exp for exp in expirations if  cutlow(exp) and cuthigh(exp) ]

        if not filtered_expirations: 
            self.option_chains = None
        else:
            self.option_chains = {}
            for expiration in filtered_expirations:
                option_chain = self.stock_obj.option_chain(expiration)
                self.option_chains[expiration] = option_chain

        return self.option_chains#, self.stock_obj, low_cutoff_date, high_cutoff_date, expirations, high_days_cutoff, self.stock_obj.options

    def get_expirations(self):
        return self.stock_obj.options
    
    def get_otm_puts(self, expiration_date):
        puts = self.option_chains[expiration_date].puts
        puts = puts[puts.inTheMoney==False]
        puts=puts.sort_values(by='strike', ascending=False)
        self.otm_puts = puts
        return self.otm_puts
