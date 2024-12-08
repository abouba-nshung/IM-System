from kafka import KafkaProducer
import json
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Kafka broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize messages as JSON
)


def publish_message(topic, message, key=None):
    """
    Publish a message to a Kafka topic.

    Args:
        topic (str): Kafka topic name.
        message (dict): Message payload (Python dictionary).
        key (str, optional): Optional message key for partitioning.
    """
    try:
        producer.send(topic, key=key.encode('utf-8') if key else None, value=message)
        producer.flush()  # Ensure message is sent
        logger.info(f"Message published to topic {topic}: {message}")
    except Exception as e:
        logger.error(f"Error publishing message to topic {topic}: {e}", exc_info=True)


# Example Usage
if __name__ == "__main__":
    # Example message
    message = {"event": "test_event", "data": {"id": 1, "value": "Hello Kafka"}}
    publish_message("test_topic", message)

