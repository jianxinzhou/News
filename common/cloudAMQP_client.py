''' cloud AMQP client module '''

import json
import pika

class CloudAMQPClient:
    ''' cloud AMQP client '''
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.ConnectionParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)

    def publish(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        print "[x] Sent message to %s %s" % (self.queue_name, message)

    def sendMessage(self, message):
        ''' send a message '''
        # https://stackoverflow.com/questions/35193335/how-to-reconnect-to-rabbitmq
        try:
            self.publish(message)
        except pika.exceptions.ConnectionClosed:
            print "reconnecting to queue"
            self.connect()
            self.publish(message)

    def getMessage(self):
        ''' get a message '''
        method_frame, header_frame, body = self.channel.basic_get(
            self.queue_name)
        if method_frame:
            print "[x] Received message from %s: %s" % (self.queue_name, body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body)
        else:
            print "No message returned"
            return None

    def sleep(self, seconds):
        ''' sleep seconds to keep connection '''
        self.connection.sleep(seconds)
