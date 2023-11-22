import json
import requests
from config import currencies

class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')
        try:
            base_ticker = currencies[base.lower()]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена.')
        try:
            quote_ticker = currencies[quote.lower()]
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена.')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        total_price = json.loads(r.content)[quote_ticker] * amount
        return round(total_price, 2)
