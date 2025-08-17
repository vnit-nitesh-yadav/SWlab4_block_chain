import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a transaction queue
channel.queue_declare(queue='transaction', durable=True)

def send_transaction(transaction):
    message = json.dumps(transaction)
    channel.basic_publish(
        exchange='',
        routing_key='transaction',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    print(f" [x] Sent transaction: {message}")

transaction = {
    "sender": "Alice",
    "receiver": "Bob",
    "amount": 100
}

send_transaction(transaction)
connection.close()