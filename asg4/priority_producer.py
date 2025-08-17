import pika
import random

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue with priority support (max priority = 10)
args = {'x-max-priority': 10}
channel.queue_declare(queue='priority_queue', durable=True, arguments=args)

# Define messages with different priorities
messages = [
    ("Low Priority Message", 1),
    ("Medium Priority Message", 5),
    ("High Priority Message", 10),
    ("Another Low Priority Message", 2),
    ("Critical Message", 9)
]

# Send messages
for msg, priority in messages:
    channel.basic_publish(
        exchange='',
        routing_key='priority_queue',
        body=msg,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
            priority=priority  # Assign priority
        )
    )
    print(f"[Producer] Sent: {msg} (Priority: {priority})")

# Close connection
connection.close()
