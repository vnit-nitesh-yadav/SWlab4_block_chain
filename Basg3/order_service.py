import pika
import json
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare an exchange for fanout (broadcasting)
channel.exchange_declare(exchange='order_exchange', exchange_type='fanout')

# Simulate an order placement
order = {"order_id": 102, "item": "Mobile", "quantity": 2}
message = json.dumps(order)

# Publish order event
channel.basic_publish(exchange='order_exchange', routing_key='', body=message)
print(f"[✓] Order placed: {message}")

# Close connection
connection.close()