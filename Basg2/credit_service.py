import pika
import json
import random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='credit', durable=True)
channel.queue_declare(queue='rollback', durable=True)

def process_credit(ch, method, properties, body):
    transaction = json.loads(body)
    
    # Simulating failure scenario
    if random.choice([True, False]):  # Randomly fail the transaction
        print(f" [!] Credit failed for {transaction['receiver']}. Rolling back...")
        channel.basic_publish(
            exchange='', routing_key='rollback', body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print(f" [x] Credited {transaction['amount']} to {transaction['receiver']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='credit', on_message_callback=process_credit)
print(" [*] Waiting for transactions to credit...")
channel.start_consuming()