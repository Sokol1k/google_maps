import pika
import logging
import os
import json
from database.Connection import Connection
from scrapy.commands import ScrapyCommand

logger = logging.getLogger(__name__)


class AddedItemsToDB(ScrapyCommand):
    def __init__(self, *a, **kw):
        self.db = Connection()
        self.url = os.getenv('RABBIT_URL')
        self.queue = os.getenv('RABBIT_ITEMS_QUEUE')
        self.exchange = os.getenv('RABBIT_ITEMS_EXCHANGE')
        self.routing_key = os.getenv('RABBIT_ITEMS_ROUNTING_KEY')

    def run(self, args, opts):
        parameters = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(parameters=parameters)
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.exchange_declare(exchange=self.exchange, durable=True)
        self.channel.queue_bind(queue=self.queue,
                                exchange=self.exchange, routing_key=self.routing_key)
        self.channel.basic_consume(self.queue, self.add_to_db)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

    def add_to_db(self, ch, method, properties, body):
        sector = json.loads(body)
        self.db.add_item(sector)
        self.channel.basic_ack(method.delivery_tag)

# scrapy AddedItemsToDB -L WARNING
