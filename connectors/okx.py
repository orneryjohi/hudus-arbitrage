import ccxt


class OKXConnector:
    def __init__(self):
        self.exchange = ccxt.okx()

    def get_price(self, symbol="BTC/USDT"):
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker["last"]