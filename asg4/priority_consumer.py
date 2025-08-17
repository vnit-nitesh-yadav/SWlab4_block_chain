import pika
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue (must match producer's queue)
args = {'x-max-priority': 10}
channel.queue_declare(queue='priority_queue', durable=True, arguments=args)

print("[Consumer] Waiting for messages...")

def callback(ch, method, properties, body):
    msg = body.decode()
    print(f"[Consumer] Processing: {msg}")

    # Simulate processing time
    time.sleep(2)
    
    print(f"[Consumer] Completed: {msg}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='priority_queue', on_message_callback=callback)

channel.start_consuming()
