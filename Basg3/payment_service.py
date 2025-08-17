import pika
import json
import random
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue and bind to exchange
channel.queue_declare(queue='payment_queue')
channel.queue_bind(exchange='order_exchange', queue='payment_queue')

print("[*] Waiting for payment processing...")

# Callback function to process payment
def callback(ch, method, properties, body):
    order = json.loads(body)
    order_id = order["order_id"]

    print(f"[✓] Processing payment for Order ID {order_id}...")

    # Simulate random payment success/failure
    success = random.choice([True, False])

    time.sleep(2)  # Simulate processing delay

    if success:
        print(f"[✓] Payment successful for Order ID {order_id}.")
    else:
        print(f"[!] Payment failed for Order ID {order_id}. Rolling back...")

# Start consuming messages
channel.basic_consume(queue='payment_queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()