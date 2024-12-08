from django.core.management.base import BaseCommand
from inventory.kafka_consumer import consume_messages
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Start Kafka consumer for a specific topic'

    def add_arguments(self, parser):
        """
        Add command-line arguments to customize the consumer behavior.
        """
        parser.add_argument(
            '--topic',
            type=str,
            default='inventory_topic',
            help='Kafka topic to consume messages from (default: inventory_topic)'
        )
        parser.add_argument(
            '--group_id',
            type=str,
            default='inventory_app',
            help='Consumer group ID (default: inventory_app)'
        )
        parser.add_argument(
            '--bootstrap_servers',
            type=str,
            default='localhost:9092',
            help='Kafka broker address (default: localhost:9092)'
        )

    def handle(self, *args, **options):
        """
        Handle the execution of the command.
        """
        topic = options['topic']
        group_id = options['group_id']
        bootstrap_servers = options['bootstrap_servers']

        logger.info(f"Starting Kafka consumer for topic '{topic}' with group ID '{group_id}'")
        try:
            consume_messages(topic, group_id=group_id, bootstrap_servers=bootstrap_servers)
        except Exception as e:
            logger.error(f"Error while starting Kafka consumer: {e}", exc_info=True)


