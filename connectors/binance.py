import ccxt


class BinanceConnector:
    def __init__(self):
        self.exchange = ccxt.binance()

    def get_price(self, symbol="BTC/USDT"):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker["last"]