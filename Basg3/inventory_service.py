import pika
import json

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue and bind to exchange
channel.queue_declare(queue='inventory_queue')
channel.queue_bind(exchange='order_exchange', queue='inventory_queue')

print("[*] Waiting for order events...")

# Inventory Database (mock)
stock = {"Laptop": 10, "Phone": 5}

# Callback function to process message
def callback(ch, method, properties, body):
    order = json.loads(body)
    item = order["item"]
    
    if item in stock and stock[item] > 0:
        stock[item] -= 1
        print(f"[✓] Stock updated for {item} (Remaining: {stock[item]})")
    else:
        print(f"[!] Out of stock for {item}")

# Start consuming messages
channel.basic_consume(queue='inventory_queue', on_message_callback=callback, auto_ack=True)
channel.start_consuming()