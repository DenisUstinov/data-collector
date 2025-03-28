import json
import logging
from .models import Trade, Ticker, Order
from .config import SPOT_TRADES_TOPIC, SPOT_TICKER_TOPIC, SPOT_ORDER_BOOK_SNAPSHOTS_TOPIC

logger = logging.getLogger(__name__)

class Handler:
    def __init__(self, db):
        self.db = db

    async def response_handler(self, response: str):
        try:
            data = json.loads(response)
            ts = data.get("ts")
            if data.get("event") == "update":
                topic = data.get("topic")
                pair = topic.split(":")[1]

                if topic.startswith(SPOT_TRADES_TOPIC,):
                    for item in data["data"]:
                        item["ts"] = ts
                        item["pair"] = pair
                        item.pop("date", None)
                        await self.process(Trade, Handler.process_trade_data(item))
                elif topic.startswith(SPOT_TICKER_TOPIC):
                    item = data["data"]
                    item.pop("updated", None)
                    item["ts"] = ts
                    item["pair"] = pair
                    await self.process(Ticker, Handler.process_ticker_data(item))
                elif topic.startswith(SPOT_ORDER_BOOK_SNAPSHOTS_TOPIC) or topic.startswith("orders"):
                    item = data["data"]
                    item["ts"] = ts
                    item["pair"] = pair
                    await self.process(Order, Handler.process_order_data(item))
        except Exception as e:
            logger.exception(f"Error processing message: {e}")

    async def process(self, model, data):
        try:
            await self.db.insert_record(model, data)
        except Exception as e:
            logger.exception(f"Error processing {model.__name__}: {e}")

    @classmethod
    def process_trade_data(cls, data):
        return {
            'pair': data['pair'],
            'trade_id': int(data['trade_id']),
            'type': data['type'],
            'price': float(data['price']),
            'quantity': float(data['quantity']),
            'amount': float(data['amount']),
            'ts': int(data['ts'])
        }

    @classmethod
    def process_ticker_data(cls, data):
        return {
            'pair': data['pair'],
            'buy_price': float(data['buy_price']),
            'sell_price': float(data['sell_price']),
            'last_trade': float(data['last_trade']),
            'high': float(data['high']),
            'low': float(data['low']),
            'avg': float(data['avg']),
            'vol': float(data['vol']),
            'vol_curr': float(data['vol_curr']),
            'ts': int(data['ts'])
        }

    @classmethod
    def process_order_data(cls, data):
        ask = data['ask'][0]
        bid = data['bid'][0]
        
        return {
            'pair': data['pair'],
            'ask_price': float(ask[0]),
            'ask_quantity': float(ask[1]),
            'ask_amount': float(ask[2]),
            'bid_price': float(bid[0]),
            'bid_quantity': float(bid[1]),
            'bid_amount': float(bid[2]),
            'ts': int(data['ts'])
        }