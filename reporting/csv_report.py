import csv
import os

from datetime import datetime


class CSVReport:

    def save(self, opportunities):

        os.makedirs("results", exist_ok=True)

        filename = datetime.now().strftime(
            "results/%Y-%m-%d_%H-%M-%S.csv"
        )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Pair",
                "Buy Exchange",
                "Sell Exchange",
                "Buy Price",
                "Sell Price",
                "Spread %"
            ])

            for opportunity in opportunities:

                writer.writerow([
                    opportunity.pair,
                    opportunity.buy_exchange,
                    opportunity.sell_exchange,
                    opportunity.buy_price,
                    opportunity.sell_price,
                    round(opportunity.percent, 5)
                ])

        return filename