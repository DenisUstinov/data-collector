import json

DATA = {
    "url": "wss://ws-api.exmo.com:443/v1/public",
    "pairs": [
        "BTC_USDT",
        "ETH_USDT",
        "BTC_ETH",
    ],
    "init_messages": [
        {
            "method": "subscribe",
            "topics": [
                "spot/trades:",
                "spot/ticker:",
                "spot/order_book_snapshots:",
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
