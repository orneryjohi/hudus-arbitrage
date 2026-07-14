from models.opportunity import Opportunity


class SpreadCalculator:

    def calculate(self, pair, prices):

        valid_prices = {
            exchange: price
            for exchange, price in prices.items()
            if price is not None
        }

        if len(valid_prices) < 2:
            return None

        buy_exchange = min(
            valid_prices,
            key=valid_prices.get
        )

        sell_exchange = max(
            valid_prices,
            key=valid_prices.get
        )

        buy_price = valid_prices[buy_exchange]
        sell_price = valid_prices[sell_exchange]

        difference = sell_price - buy_price
        percent = (difference / buy_price) * 100

        # Отсекаем очевидные ошибки
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