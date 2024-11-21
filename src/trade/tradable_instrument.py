import trade.options as options
import trade.stocks as stocks

class TradableInstrument:
    def __init__(self, ticker):
        self.stock = stocks.Stocks(ticker=ticker)
        self.options = options.Options(ticker=ticker)