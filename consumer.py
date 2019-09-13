#!/usr/bin/env python

import pika
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PWD = os.getenv("RABBIT_PWD")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME")
QUEUE_NAME = os.getenv("QUEUE_NAME")

credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PWD)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE

parameters = pika.ConnectionParameters(
    credentials=credentials,
    ssl_options=pika.SSLOptions(context),
    host=RABBIT_HOST,
    virtual_host=RABBIT_USER  # CloudAMQP sets the vhost same as User
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(queue=QUEUE_NAME,
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
