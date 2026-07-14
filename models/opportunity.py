class Opportunity:

    def __init__(
        self,
        pair,
        prices,
        buy_exchange,
        sell_exchange,
        buy_price,
        sell_price,
        difference,
        percent
    ):
        self.pair = pair
        self.prices = prices

        self.buy_exchange = buy_exchange
        self.sell_exchange = sell_exchange

        self.buy_price = buy_price
        self.sell_price = sell_price

        self.difference = difference
        self.percent = percent