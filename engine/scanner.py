class Scanner:
    def compare(self, first_price, second_price):
        difference = second_price - first_price
        percent = (difference / first_price) * 100

        return difference, percent