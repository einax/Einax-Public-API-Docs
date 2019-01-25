import time
import hmac
import urllib
import hashlib
import requests  # pip install requests

# Create your own api_key and api_secret here: https://einax.com/users/security/api-keys/
api_key = "3e2cc318b90b99be9efe903a5f18dee4162109bf"  # you must create your own api_key!
api_secret = "ffbdab35db1d39e3b92190bfc9754034347c4b57"  # you must create your own api_secret!


def create_order_demo():
    endpoint_url = "https://einax.com/api/v1/bots/order/create/"

    post_data = {
        "timestamp": str(int(time.time() * 1000)),  # timestamp must be in milliseconds
        "recv_window": 5000,  # also milliseconds
        "market": "TICO:ETH",
        "side": "sell",
        "type": "limit",
        "quantity": "0.1",
        "price": "0.1"
    }

    rest_data_string = urllib.parse.urlencode(post_data)  # converting post_data to query string
    rest_data_bytes = rest_data_string.encode('utf-8')  # converting query string to bytes
    signature = hmac.HMAC(api_secret.encode('utf-8'), rest_data_bytes, hashlib.sha256).digest().hex().lower()
    post_data["signature"] = signature
    headers = {"X-MBX-APIKEY": api_key}
    r = requests.post(endpoint_url, data=post_data, headers=headers).text
    print(r)


create_order_demo()
