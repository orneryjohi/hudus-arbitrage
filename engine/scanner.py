from connectors.binance import BinanceConnector
from connectors.bybit import BybitConnector
from connectors.okx import OKXConnector
from models.opportunity import Opportunity


class Scanner:

    def __init__(self):

        self.binance = BinanceConnector()
        self.bybit = BybitConnector()
        self.okx = OKXConnector()

    def load_all_markets(self):

        print("Loading markets...\n")

        self.binance_markets = self.binance.load_markets()
        self.bybit_markets = self.bybit.load_markets()
        self.okx_markets = self.okx.load_markets()

        print(f"Binance : {len(self.binance_markets)} markets")
        print(f"Bybit   : {len(self.bybit_markets)} markets")
        print(f"OKX     : {len(self.okx_markets)} markets")

    def load_all_prices(self):

        print("\nLoading tickers...\n")

        self.binance_prices = self.binance.get_all_tickers()
        self.bybit_prices = self.bybit.get_all_tickers()
        self.okx_prices = self.okx.get_all_tickers()

        print(f"Binance : {len(self.binance_prices)} tickers")
        print(f"Bybit   : {len(self.bybit_prices)} tickers")
        print(f"OKX     : {len(self.okx_prices)} tickers")

    def get_common_pairs(self):

        binance_pairs = set(self.binance_markets.keys())
        bybit_pairs = set(self.bybit_markets.keys())
        okx_pairs = set(self.okx_markets.keys())

        common_pairs = (
            binance_pairs
            & bybit_pairs
            & okx_pairs
        )

        filtered = []

        for pair in common_pairs:

            if ":" in pair:
                continue

            if not pair.endswith("/USDT"):
                continue

            filtered.append(pair)

        return sorted(filtered)

    def get_prices(self, pair):

        prices = {}

        prices["Binance"] = self.binance_prices.get(pair)
        prices["Bybit"] = self.bybit_prices.get(pair)
        prices["OKX"] = self.okx_prices.get(pair)

        return prices

    def find_opportunity(self, pair):

        prices = self.get_prices(pair)

        valid_prices = {
            exchange: price
            for exchange, price in prices.items()
            if price is not None
        }

        if len(valid_prices) < 2:
            return None

        buy_exchange = min(valid_prices, key=valid_prices.get)
        sell_exchange = max(valid_prices, key=valid_prices.get)

        buy_price = valid_prices[buy_exchange]
        sell_price = valid_prices[sell_exchange]

        difference = sell_price - buy_price
        percent = (difference / buy_price) * 100

        if percent > 5:
            return None

        return Opportunity(
            pair,
            prices,
            buy_exchange,
            sell_exchange,
            buy_price,
            sell_price,
            difference,
            percent
        )

    def scan(self):

        print("=" * 40)
        print("Hudus Arbitrage Scanner")
        print("=" * 40)

        self.load_all_markets()
        self.load_all_prices()

        common_pairs = self.get_common_pairs()

        print()
        print("-" * 40)
        print(f"Common Spot USDT pairs : {len(common_pairs)}")
        print("-" * 40)

        opportunities = []

        for pair in common_pairs:

            opportunity = self.find_opportunity(pair)

            if opportunity is not None:
                opportunities.append(opportunity)

        opportunities.sort(
            key=lambda x: x.percent,
            reverse=True
        )

        print()
        print("=" * 40)
        print("TOP 20 SPREADS")
        print("=" * 40)

        for opportunity in opportunities[:20]:

            print()

            print(opportunity.pair)

            print(
                f"BUY  : {opportunity.buy_exchange:<8} {opportunity.buy_price}"
            )

            print(
                f"SELL : {opportunity.sell_exchange:<8} {opportunity.sell_price}"
            )

            print(
                f"SPREAD : {opportunity.percent:.5f}%"
            )