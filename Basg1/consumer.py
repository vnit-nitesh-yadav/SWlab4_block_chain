import pika
import time
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare task queue again
channel.queue_declare(queue='task_queue', durable=True, arguments={
    'x-dead-letter-exchange': 'dlx_exchange',
    'x-dead-letter-routing-key': 'dlx_routing_key'
})

def process_message(ch, method, properties, body):
    message = body.decode()
    headers = properties.headers or {}
    retry_count = headers.get('x-retry-count', 0)

    print(f" [!] Received: {message}, Retry: {retry_count}")

    if retry_count < 3:  # Retry message 3 times
        retry_count += 1
        delay = 2 ** retry_count  # Exponential backoff (2, 4, 8 seconds)
        
        print(f" [!] Simulating failure... Requeueing in {delay} seconds")
        time.sleep(delay)

        # Republish with updated retry count
        ch.basic_publish(
            exchange='main_exchange',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                headers={'x-retry-count': retry_count},
                delivery_mode=2  # Make message persistent
            )
        )
    else:
        print(f" [x] Moving to Dead Letter Queue: {message}")
        ch.basic_publish(
            exchange='dlx_exchange',
            routing_key='dlx_routing_key',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='task_queue', on_message_callback=process_message)

print(' [*] Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
