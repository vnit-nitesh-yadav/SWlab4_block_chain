import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='rollback', durable=True)

def process_rollback(ch, method, properties, body):
    transaction = json.loads(body)
    print(f" [!] Rolling back transaction: {transaction}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='rollback', on_message_callback=process_rollback)
print(" [*] Waiting for failed transactions to roll back...")
channel.start_consuming()