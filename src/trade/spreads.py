import pandas as pd

class OTMPutSpreads:
    
    def __init__(self, ticker='GOOG', credit_risk_margin=.1):
        self.credit_risk_margin = credit_risk_margin
        self.ticker = ticker
        
    def find_put_spread(self, puts_f, last_f):

        short_put_candidates = puts_f[puts_f['strike'] <= last_f]
        put_spreads = []
        for _, short_put in short_put_candidates.iterrows():
            long_put_candidates = puts_f[puts_f['strike'] < short_put['strike']]
            if not long_put_candidates.empty:
                long_put = long_put_candidates.iloc[0]  # Get the first available long put

                # Calculate credit and risk
                short_price = (short_put['bid']*.8 + short_put['ask']*.2)
                long_price = (long_put['bid']*.2+long_put['ask']*.8)
                credit = short_price - long_price
                risk = short_put['strike'] - long_put['strike'] - credit

                # Check if credit is greater than 50% of the risk   
                if credit > self.credit_risk_margin * risk:
                    put_spreads.append({
                        #'short_put_contract': short_put['contractSymbol'],
                        'ticker':self.ticker,
                        'last_price':last_f,
                        'short_strike': short_put['strike'],
                        'long_strike': long_put['strike'],
                        'credit': credit,
                        'risk': risk,
                        'c/r': credit/risk,
                        'ITM_return':(short_put['strike']-last_f)/last_f, 

                        'short_bid':short_put['bid'],
                        'short_ask':short_put['ask'],
                        'short_price':short_price,                        
                        'long_bid':long_put['bid'],
                        'long_ask':long_put['ask'],
                        'long_price':long_price,
                        
                        
                        #'market_credit':market_credit,
                        
                        #'market_risk':market_risk,
                        
                        #'market_c/r':market_credit/market_risk,
                        
                        'expected_return':''             
                    })

        return pd.DataFrame(put_spreads)