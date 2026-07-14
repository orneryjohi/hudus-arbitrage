from connectors.bybit import BybitConnector
from connectors.okx import OKXConnector
from engine.scanner import Scanner


def main():
    print("=" * 40)
    print("Hudus Arbitrage v0.1")
    print("System initialized")
    print("=" * 40)

    # Подключаемся к биржам
    bybit = BybitConnector()
    okx = OKXConnector()

    # Получаем цены
    bybit_price = bybit.get_price("BTC/USDT")
    okx_price = okx.get_price("BTC/USDT")

    # Создаём сканер
    scanner = Scanner()

    # Считаем разницу
    difference, percent = scanner.compare(
        bybit_price,
        okx_price
    )

    # Выводим результат
    print()
    print(f"Bybit      : {bybit_price:.2f}")
    print(f"OKX         : {okx_price:.2f}")
    print("-" * 40)
    print(f"Difference : {difference:.2f} USDT")
    print(f"Spread      : {percent:.5f}%")


if __name__ == "__main__":
    main()