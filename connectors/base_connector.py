import ccxt


class BaseConnector:
    exchange_id = None
    exchange_name = None
    taker_fee = 0.001

    def __init__(self):
        if not self.exchange_id:
            raise ValueError("exchange_id must be defined in subclass")

        exchange_factory = getattr(ccxt, self.exchange_id)
        self.exchange = exchange_factory()

    def load_markets(self):
        return self.exchange.load_markets()

    def get_all_tickers(self):
        if not getattr(self.exchange, "markets", None):
            self.exchange.load_markets()

        tickers = self.exchange.fetch_tickers()
        prices = {}

        for symbol, ticker in tickers.items():
            bid = ticker.get("bid")
            ask = ticker.get("ask")
            last = ticker.get("last")

            if bid is None and ask is None and last is None:
                continue

            prices[symbol] = {
                "bid": bid,
                "ask": ask,
                "last": last,
            }

        return prices