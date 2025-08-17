import pika
import json

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue and bind to exchange
channel.queue_declare(queue='notification_queue')
channel.queue_bind(exchange='order_exchange', queue='notification_queue')

print("[*] Waiting for notifications...")

# Callback function to process message
def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f"[✓] Confirmation sent for Order ID {order['order_id']}.")

# Start consuming messages
channel.basic_consume(queue='notification_queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()