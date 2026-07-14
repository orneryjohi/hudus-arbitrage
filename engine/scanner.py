from time import perf_counter

from connectors.binance import BinanceConnector
from connectors.bybit import BybitConnector
from connectors.okx import OKXConnector
from engine.spread_calculator import SpreadCalculator


class Scanner:

    def __init__(self):

        self.binance = BinanceConnector()
        self.bybit = BybitConnector()
        self.okx = OKXConnector()

        self.calculator = SpreadCalculator()

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

        common_pairs = (
            set(self.binance_markets.keys())
            & set(self.bybit_markets.keys())
            & set(self.okx_markets.keys())
        )

        return sorted(
            pair
            for pair in common_pairs
            if pair.endswith("/USDT") and ":" not in pair
        )

    def get_prices(self, pair):

        return {
            "Binance": self.binance_prices.get(pair),
            "Bybit": self.bybit_prices.get(pair),
            "OKX": self.okx_prices.get(pair),
        }

    def scan(self):

        start = perf_counter()

        print("=" * 60)
        print("Hudus Arbitrage Scanner")
        print("=" * 60)

        self.load_all_markets()
        self.load_all_prices()

        common_pairs = self.get_common_pairs()

        opportunities = []

        for pair in common_pairs:

            prices = self.get_prices(pair)

            opportunity = self.calculator.calculate(pair, prices)

            if opportunity:
                opportunities.append(opportunity)

        opportunities.sort(
            key=lambda x: x.percent,
            reverse=True
        )

        print()
        print("=" * 60)
        print(f"{'PAIR':<18}{'BUY':<12}{'SELL':<12}{'SPREAD'}")
        print("=" * 60)

        for opportunity in opportunities[:20]:

            print(
                f"{opportunity.pair:<18}"
                f"{opportunity.buy_exchange:<12}"
                f"{opportunity.sell_exchange:<12}"
                f"{opportunity.percent:.5f}%"
            )

        end = perf_counter()

        print("=" * 60)
        print(f"Scanned pairs : {len(common_pairs)}")
        print(f"Found spreads : {len(opportunities)}")
        print(f"Execution time: {end-start:.2f} sec")
        print("=" * 60)