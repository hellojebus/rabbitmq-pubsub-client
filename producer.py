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
channel.queue_declare(QUEUE_NAME)
channel.basic_publish(exchange=QUEUE_NAME,
                      routing_key="",
                      body='Hello World #3!')

print(" [x] Sent 'Hello World #3!'")
connection.close()