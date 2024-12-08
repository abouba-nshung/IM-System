from kafka import KafkaConsumer
import json
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def consume_messages(topic, group_id='inventory_app', bootstrap_servers='localhost:9092'):
    """
    Consume messages from a Kafka topic.

    Args:
        topic (str): Kafka topic to consume messages from.
        group_id (str): Consumer group ID.
        bootstrap_servers (str): Kafka broker address.
    """
    try:
        # Initialize Kafka consumer
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        logger.info(f"Listening to messages on topic: {topic} with group ID: {group_id}")
        for message in consumer:
            logger.info(f"Received message: {message.value}")
    except Exception as e:
        logger.error(f"Error consuming messages: {e}", exc_info=True)

# Example Usage
if __name__ == "__main__":
    # Topic to listen to
    topic = "test_topic"
    consume_messages(topic)
