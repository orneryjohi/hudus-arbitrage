import ccxt


class BinanceConnector:

    def __init__(self):
        self.exchange = ccxt.binance()

    def load_markets(self):
        return self.exchange.load_markets()

    def get_all_tickers(self):

        tickers = self.exchange.fetch_tickers()

        prices = {}

        for symbol, ticker in tickers.items():

            last = ticker.get("last")

            if last is not None:
                prices[symbol] = last

        return prices

    def get_price(self, symbol):

        prices = self.get_all_tickers()

        return prices.get(symbol)