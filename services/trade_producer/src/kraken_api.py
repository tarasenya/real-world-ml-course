from typing import List, Dict, Optional
import json
from websocket import create_connection


class KrakenWebsocketTradeAPI:
    URL = "wss://ws.kraken.com/v2"

    def __init__(self, product_id: Optional[str] = None):
        self.product_id = product_id
        self._ws = create_connection(self.URL)
        print("Connection established")
        if self.product_id:
            self._subscribe(product_id=product_id)
        else:
            product_pairs = self.get_all_possible_trade_pairs()
            for pair in product_pairs:
                self._subscribe(product_id=pair)

    def _subscribe(self, product_id: str):
        print(f"Subscribing to trades for {product_id}")
        msg = {
            "method": "subscribe",
            "params": {
                "channel": "trade",
                "symbol": [
                    product_id,
                ],
            },
        }
        self._ws.send(json.dumps(msg))
        print("Subscription worked!")

        # dumping the first 2 messages we got from the websocket, because they contain
        # no trade data, just confirmation on their end that the subscription was successful
        _ = self._ws.recv()
        _ = self._ws.recv()

    def get_trades(self) -> List[Dict]:
        """
        Retrieves the latest trade data from the Kraken API.

        Returns:
            A list of dictionaries representing the trades. Each
            dictionary contains the following fields:
            - 'product_id': The ID of the product.
            - 'price': The price of the trade.
            - 'volume': The volume of the trade.
            - 'timestamp': The timestamp of the trade.
        """
        message = self._ws.recv()

        if "heartbeat" in message:
            # when I get a heartbeat, I return an empty list
            return []

            # parse the message string as a dictionary
        message = json.loads(message)

        # extract trades from the message['data'] field
        trades = []
        for trade in message["data"]:
            try:
                trades.append(
                    {
                        "product_id": self.product_id,
                        "price": trade["price"],
                        "volume": trade["qty"],
                        "timestamp": trade["timestamp"],
                    }
                )
            except TypeError:
                print("Error parsing trade")
                print(trade)

        return trades

    def get_all_possible_trade_pairs(self) -> List[str]:
        """
        Retrieves all possible trade pairs from the Kraken API.

        Returns:
            A list of strings representing all possible trade pairs.
        """
        msg = {
            "method": "subscribe",
            "params": {
                "channel": "instrument",
            },
        }
        self._ws.send(json.dumps(msg))
        _ = self._ws.recv()
        _ = self._ws.recv()
        message = self._ws.recv()
        message = json.loads(message)
        list_of_pairs = list(map(lambda x: x["symbol"], message["data"]["pairs"]))
        return list_of_pairs
