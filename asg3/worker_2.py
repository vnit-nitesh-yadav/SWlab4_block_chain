import pika
import time
import random

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare queue (must be same as producer)
channel.queue_declare(queue='task_queue', durable=True)

print("[Worker 2] Waiting for tasks...")

def callback(ch, method, properties, body):
    task = body.decode()
    print(f"[Worker 2] Processing: {task}")
    
    # Simulate task processing time
    time.sleep(random.randint(2, 5))
    
    print(f"[Worker 2] Completed: {task}")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
