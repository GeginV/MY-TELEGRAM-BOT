import requests
import json
from config import keys


class ConversionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConversionException('Converted currencies should be different.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Could not process currency {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Could not process currency {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Could not process amount {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
