#!/usr/bin/env python

import pika
import ssl
import os
import random
from dotenv import load_dotenv

load_dotenv()

RABBIT_HOST = os.getenv("RABBIT_HOST")
RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PWD = os.getenv("RABBIT_PWD")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME")
QUEUE_NAME = os.getenv("QUEUE_NAME")

RANDOM_INT = random.randint(1,1000)
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
channel.queue_declare(queue=QUEUE_NAME, durable=True)
channel.basic_publish(exchange=EXCHANGE_NAME,
                      routing_key="",
                      body='Hello World {}!'.format(RANDOM_INT))

print(" [x] Sent 'Hello World {}!'".format(RANDOM_INT))
connection.close()