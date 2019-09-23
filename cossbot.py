# Todo doc
import urllib.parse
import hashlib
import hmac
import json
import requests
import time
from urllib.parse import urlencode


class CossBot():

    def __init__(self):
        self.API_PUBLIC = 'QUZoRzhPL0NjcDdqczdWcUVDd0lrTFJtcFhKS0JhNG9rSHcxZWJsWUF1MW0yakRncWdsWmxqMHZ2Q05DVU5KTDFycFo0anczV1lwV2dYbFArckFhWU8vdThmMTdhMUp2SEVDbHRsSTFKNUk9'
        self.API_SECRET = bytes('a6aMLqbglJzUsVcIK8mvH5oQcF+ZXQ5AVpg+kPmS8QA=','utf-8')
        self.TRADE_URL = "https://trade.coss.io/c/api/v1"
        self.EXCHANGE_URL = "https://exchange.coss.io/api"
        self.ENGINE_URL = "https://engine.coss.io/api/v1"
        self.order_headers = {"Content-Type": "application/json",
                              "Authorization": self.API_PUBLIC,
                              "Signature": None}
        self.s = requests.Session()

    
    def sign(self, payload):

        try:
            qs_payload = urllib.parse.urlencode(payload)
            signature = hmac.new(self.API_SECRET, qs_payload.encode('utf8'), hashlib.sha256).hexdigest()
        except Exception as e:
            print(e)
            return False

        return signature


    def get_market_price(self, symbol=None):
        """Retrieves market price informations for a symbol/all symbols

        If a symbol is provided then retrieves market-price for the symbol,
        else, retrieves market-price for all symbols.

        args:
            symbol(str): 'ETH_BTC'

        Returns:
            Dict : {
                "symbol": "ETH_BTC",
                "price": "0.01234567",
                "updated_time": 1538116102137
            }
        """

        if symbol:
            return self.s.get(
                    self.TRADE_URL + "/market-price",
                    params={'symbol': symbol}
                ).json()

        return self.s.get(self.TRADE_URL + "/market-price").json()


    def get_market_summaries(self):
        """Retrieves market summaries for all pairs

        Returns:
            "result": [
                {
                    "MarketName": "ETH_BTC",
                    "High": 0.00018348,
                    "Low": 0.00015765,
                    "BaseVolume": 240.82775523,
                    "Last": 0.00017166,
                    ...
                    }
                ],
                "volumes": [
                {
                    "CoinName": "BTC",
                    "Volume": 571.64749041
                }
            ],
            "t": 1531208813959
        """

        return self.s.get(self.EXCHANGE_URL + "/getmarketsummaries").json()


    def get_market_depth(self, symbol=None):
        """retrieves depth for a pair

        args:
            symbol(str): "ETH_BTC"

        returns:
            {
                "symbol": "COSS_ETH",
                "limit": 10,
                "asks": [
                    [
                        "0.12345678",
                        "0.00234567"
                    ]
                ],
                "bids": [
                    [
                        "0.12345678",
                        "0.00234567"
                    ]
                ],
                "time": 1538114348750
            }
        """

        if symbol:
            return self.s.get(
                self.ENGINE_URL + "/dp",
                params={'symbol': symbol}
            ).json()

        return "no symbol provided"


    def get_market_information(self, symbol=None):
        """Retrieves market information for a given symbol

        returns:
            {
                "symbol": "ETH_BTC",
                "limit": 100,
                "history": [
                    {
                        "id": 139638,
                        "price": "0.00001723",
                        "qty": "81.00000000",
                        "isBuyerMaker": false,
                        "time": 1529262196270
                    }
                ],
                "time": 1529298130192
            }
        """

        if symbol:
            return self.s.get(self.ENGINE_URL + "/ht",
                params={'symbol': symbol}
                ).json()

        return "no symbol provided"


    def get_exchange_information(self):
        """Provides information about trading rules, symbols, rate limits...

        {
            "timezone": "UTC",
            "server_time": 1530683054384,
            "rate_limits": [
                {
                "type": "REQUESTS",
                "interval": "MINUTE",
                "limit": 60
                }
            ],
            "base_currencies": [
                {
                "currency_code": "COSS",
                "minimum_total_order": 100
                }
            ],
            "coins": [
                {
                "currency_code": "USDT",
                "name": "Tether",
                "minimum_order_amount": 1
                }
            ],
            "symbols": [
                {
                "symbol": "COSS_ETH",
                "amount_limit_decimal": 0,
                "price_limit_decimal": 8,
                "allow_trading": true
                }
            ]
        }
        """

        return self.s.get(self.TRADE_URL + "/exchange-info").json()


    def test_api_connection(self):
        """Test connectivity to API
        
        returns:
            {
                "result": true
            }
        """

        return self.s.get(self.TRADE_URL + "/ping").json()

    
    def test_connection_server_time(self):
        """Test connectivity to API and get server time

        returns:
            {
                "server_time": 1545196121361
            }
        """

        return self.s.get(self.TRADE_URL + "/time").json()
    

    def get_account_details(self):
        """Retrieves account details information

        returns:
            {
                "account_id": "3c05d5f4-41da-4c84-a167-XXXXXXXXX",
                "email": "xyz@email.com",
                "phone": 12345678,
                "enable_google_2fa": true,
                ...
            }
        """

        payload = {"timestamp": int(time.time() * 1000)}
        signature = self.sign(payload)

        if signature:
            self.order_headers['Signature'] = signature
            return self.s.get(
                self.TRADE_URL + "/account/details",
                headers=self.order_headers,
                params=payload
                ).json()
        
        return False


    def get_account_balance(self):
        """Retrieves account balances information

        returns:
            {
                "currency_code": "ETH_BTC",
                "address": "2MxctvXExQofAVqakPfBjKqVipfwTqwyQyF",
                "total": 1000.00275,
                "available": 994.5022,
                "in_order": 5.50055
            }
        """

        payload = {"timestamp": int(time.time() * 1000)}
        signature = self.sign(payload)

        if signature:
            self.order_headers['Signature'] = signature
            return self.s.get(
                self.TRADE_URL + "/account/balances",
                headers=self.order_headers,
                params=payload).json()

        return True


    def create_order(self, symbol, price, side, size, order_type, stop=None):
        """Place a new order for order side(BUY/SELL),
        and order type (market/limit)
        
        An order should at least contains symbol, price, side, size and type
        params:
            {
            "order_symbol": "ETH_BTC",
            "order_price": "1.00234567",
            "stop_price": "1.20134555",
            "order_side": "BUY",
            "order_size": "1000",
            "type": "limit",
            "timestamp": 1538114348750,
            "recvWindow": 5000
            }

        returns : all informations about the order
        """

        if not symbol or not price or not side or not size or not size:
            print("missing values")

        timestamp = time.time() * 1000
        print(timestamp, type(timestamp))

        order_symbol = str(symbol)
        order_price = str(price)
        order_side = str(side).upper()
        order_size = str(size)
        order_type = str(order_type).lower()
        order_stop = str(stop) if stop else None

        data = {
            "order_symbol": order_symbol,
            "order_price": order_price,
            "order_side": order_side.upper(),
            "order_size": order_size,
            "type": order_type.lower(),
            "timetamp": timestamp,
        }

        if order_stop:
            data['order_stop'] = order_stop

        payload = {"timestamp": timestamp}
        signature = self.sign(payload)

        if signature:
            self.order_headers['signature'] = signature
            request = self.s.post(self.TRADE_URL + "/order/add", headers=self.order_headers, data=data)
            return request.content

        return False


    