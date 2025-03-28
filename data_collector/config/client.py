import json

BTC_ETH_USDT_KTZ_RUB = [
    "BTC_ETH",
    "BTC_USDT",
    "ETH_USDT",
    "BTC_KTZ",
    "ETH_KTZ",
    "BTC_RUB",
    "ETH_RUB"
]

SPOT_TRADES_TOPIC = "spot/trades:"
SPOT_TICKER_TOPIC = "spot/ticker:"
SPOT_ORDER_BOOK_SNAPSHOTS_TOPIC = "spot/order_book_snapshots:"

DATA = {
    "url": "wss://ws-api.exmo.com:443/v1/public",
    "pairs": BTC_ETH_USDT_KTZ_RUB,
    "init_messages": [
        {
            "method": "subscribe",
            "topics": [
                SPOT_TRADES_TOPIC,
                SPOT_TICKER_TOPIC,
                SPOT_ORDER_BOOK_SNAPSHOTS_TOPIC,
            ]
        }
    ]
}

def transform_data(data):
    try:
        template = data['init_messages'][0]
        
        messages = []
        for idx, pair in enumerate(data['pairs'], start=1):
            msg = {
                "id": idx,
                "method": template["method"],
                "topics": [f"{topic}{pair}" for topic in template["topics"]]
            }
            messages.append(json.dumps(msg, separators=(',', ':')))
        
        return {
            "url": data["url"],
            "init_messages": messages
        }
        
    except KeyError as e:
        raise ValueError(f"Missing key: {e}") from e
    except TypeError as e:
        raise ValueError(f"Data type error: {e}") from e
    except Exception as e:
        raise ValueError(f"Transformation error: {e}") from e

DATA = transform_data(DATA)
