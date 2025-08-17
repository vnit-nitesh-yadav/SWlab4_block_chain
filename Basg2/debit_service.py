import pika
import json
import random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='transaction', durable=True)
channel.queue_declare(queue='rollback', durable=True)

def process_debit(ch, method, properties, body):
    transaction = json.loads(body)
    
    # Simulating failure scenario
    if random.choice([True, False]):  # Randomly fail the transaction
        print(f" [!] Debit failed for {transaction['sender']}. Rolling back...")
        channel.basic_publish(
            exchange='', routing_key='rollback', body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print(f" [x] Debited {transaction['amount']} from {transaction['sender']}")
    channel.basic_publish(
        exchange='', routing_key='credit', body=body,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='transaction', on_message_callback=process_debit)
print(" [*] Waiting for transactions to debit...")
channel.start_consuming()