import pika
import logging
import os
import time
import json
from database.Connection import Connection
from scrapy.commands import ScrapyCommand

logger = logging.getLogger(__name__)


class QueueForSectorsCommand(ScrapyCommand):
    def __init__(self, *a, **kw):
        self.db = Connection()
        self.url = os.getenv('RABBIT_URL')
        self.queue = os.getenv('RABBIT_SECTOR_QUEUE')
        self.exchange = os.getenv('RABBIT_SECTOR_EXCHANGE')
        self.routing_key = os.getenv('RABBIT_SECTOR_ROUNTING_KEY')
        self.max_queue_length = os.getenv('RABBIT_MAX_QUEUE_LENGTH')

    def can_add(self):
        queue = self.channel.queue_declare(
            queue=self.queue, passive=True, durable=True)
        return queue.method.message_count < int(self.max_queue_length)

    def run(self, args, opts):
        parameters = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(parameters=parameters)
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.exchange_declare(exchange=self.exchange)
        self.channel.queue_bind(queue=self.queue,
                                exchange=self.exchange, routing_key=self.routing_key)
        while True:
            if self.can_add():
                sector = self.db.get_sector()
                if sector:
                    data = {
                        'center_latitude': float(sector.center_latitude),
                        'center_longitude': float(sector.center_longitude),
                        'keyword': str(sector.keyword),
                        'id': sector.id
                    }
                    json_data = json.dumps(data)
                    try:
                        self.channel.basic_publish(exchange=self.exchange,
                                                   routing_key=self.routing_key, body=str(json_data))
                        if (self.db.change_sector_status({'id': sector.id, 'status': 1}) is None):
                            logger.error('Sector status not changed!')
                            break

                    except:
                        logger.error('Data not added to queue!')
                        break
                else:
                    logger.error('There are no sectors in the database!')
                    break
            else:
                time.sleep(1)
        connection.close()

# scrapy QueueForSectorsCommand -L WARNING