import numpy as np
import pandas as pd
from tqdm import tqdm

from trade.tradable_instrument import TradableInstrument
from trade.spreads.bull_put_spread import find_put_spread
from trade.utils import days_until

"""Next we need to package the code in this loop"""
def search_bull_put_spreads(tickers, low_days_cutoff, high_days_cutoff, margin, ):
    put_spreads_df = []
    for ticker in tqdm(tickers):
        #try:

        tradable_obj=TradableInstrument(ticker)
        option_chains = tradable_obj.options.get_option_chains_within_cutoff_days(
            low_days_cutoff=low_days_cutoff, high_days_cutoff=high_days_cutoff)
        if not option_chains:continue
        for e_d in list(option_chains.keys()):
            last, sma_10, sma_50 = tradable_obj.stock.get_current_stock_price()

            puts = tradable_obj.options.get_otm_puts(expiration_date=e_d)
            put_spread = find_put_spread(puts_f=puts, last_f=last, margin=margin)

            if not put_spread.empty: # this should be moved into find put spread function
                days = days_until(date_str=e_d)  # this should be moved into find put spread function
                return_dist = tradable_obj.stock.get_historical_returns(interval=days) # this should be moved into find put spread function
                vals = return_dist[f'{days}-Day Return'].values
                p = np.zeros(put_spread.shape[0])
                for idx, itm_val in enumerate(put_spread['ITM_return']):
                    p[idx] = 1-len(vals[vals<itm_val])/len(vals)
                return_break_even = ((put_spread['short_put_strike']-put_spread['credit']) - put_spread['last_price'])/put_spread['last_price']
                p_break_even = np.zeros(put_spread.shape[0])
                for idx, bke_val in enumerate(return_break_even):
                    p_break_even[idx] = 1-len(vals[vals<bke_val])/len(vals)

                put_spread['P(success)']=p
                put_spread['P(gain)']=p_break_even
                put_spread['P(loss)']=1-p_break_even
                put_spread['break_even_return'] = return_break_even
                put_spread["expected_value"] = p*put_spread['credit'] + (p_break_even-p)*put_spread['credit']/2 - (1-p_break_even)*put_spread['risk']
                put_spread["expected_return"] = (put_spread["expected_value"])/put_spread['risk']
                put_spread["expected_annual_return"] = (put_spread["expected_return"])/(days/365)

                put_spread["expected_market_value"] = p*put_spread['market_credit'] - (1-p)*put_spread['market_risk']
                put_spread["expected_market_return"] = (put_spread["expected_market_value"])/put_spread['market_risk']
                put_spread["expected_annual_market_return"] = (put_spread["expected_market_return"])/(days/365)

                put_spread['days']=days
                put_spread['sma_10']=sma_10
                put_spread['sma_50']=sma_50
                put_spread['ticker']=ticker
                put_spreads_df.append(put_spread)
        #except:  continue  
    output = pd.concat(put_spreads_df)
    select_positive = output['expected_annual_return']>0
    return output[select_positive].reset_index(drop=True)
  
