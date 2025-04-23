import pandas as pd
import numpy as np

def find_put_spread(puts_f, last_f, margin=.1):
 
    short_put_candidates = puts_f[puts_f['strike'] <= last_f]
    put_spreads = []
    for _, short_put in short_put_candidates.iterrows():
        long_put_candidates = puts_f[puts_f['strike'] < short_put['strike']]
        if not long_put_candidates.empty:
            for _, long_put in long_put_candidates.iterrows():
                #long_put = long_put_candidates.iloc[0]  # Get the first available long put

                # Calculate credit and risk
                short_price = (short_put['bid']*.5 + short_put['ask']*.5)
                long_price = (long_put['bid']*.5+long_put['ask']*.5)
                credit = short_price - long_price#short_put['bid'] - long_put['ask']
                market_credit = short_put['bid']-long_put['ask']
                risk = np.max([short_put['strike'] - long_put['strike'] - credit, 0.01]) 
                market_risk = np.max([short_put['strike'] - long_put['strike'] - market_credit, 0.01])

                # Check if credit is greater than 50% of the risk   
                if credit > margin * risk:
                    put_spreads.append({
                        'short_put_contract': short_put['contractSymbol'],
                        'short_put_strike': short_put['strike'],
                        'short_bid':short_put['bid'],
                        'short_ask':short_put['ask'],
                        'short_price':short_price,
                        'long_put_contract': long_put['contractSymbol'],
                        'long_put_strike': long_put['strike'],
                        'long_bid':long_put['bid'],
                        'long_ask':long_put['ask'],
                        'long_price':long_price,
                        'last_price':last_f,
                        'credit': credit,
                        'market_credit':market_credit,
                        'risk': risk,
                        'market_risk':market_risk,
                        'c/r': credit/risk,
                        'market_c/r':market_credit/market_risk,
                        'ITM_return':(short_put['strike']-last_f)/last_f, 
                        'expected_return':''             
                    })

    return pd.DataFrame(put_spreads)