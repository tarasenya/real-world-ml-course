from quixstreams import Application
from typing import List, Dict
from time import sleep

from src.kraken_api import KrakenWebsocketTradeAPI


def produce_trades(kafka_broker_addres: str, kafka_topic_name: str,) -> None:
    """
    Reads trades from the Kraken websocket API and saves them into a Kafka 
    topic.

    Args:
        kafka_broker_addres (str): The address of the Kafka broker.
        kafka_topic_name (str): The name of the Kafka topic.

    Returns:
        None
    """
    app = Application(broker_address=kafka_broker_addres)

    # the topic where we will save the trades
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    # Create an instance of the Kraken API
    kraken_api = KrakenWebsocketTradeAPI(product_id='BTC/USD')

    print('Creating the producer...')

    # Create a Producer instance
    with app.get_producer() as producer:

        while True:

            # Get the trades from the Kraken API
            trades: List[Dict] = kraken_api.get_trades()
            print('Got trades from Kraken')
            
            for trade in trades:

                # Serialize an event using the defined Topic 
                message = topic.serialize(key=trade["product_id"],
                                          value=trade)

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name,
                    value=message.value,
                    key=message.key
                )

                print('Message sent!')

            sleep(1)


if __name__ == '__main__':

    produce_trades(
        kafka_broker_addres="redpanda-0:9092",
        #kafka_broker_addres="localhost:19092",
        kafka_topic_name="trade"
    )
