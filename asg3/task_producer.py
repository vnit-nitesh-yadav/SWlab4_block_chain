import pika
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='task_queue', durable=True)

# Send tasks
tasks = ["Task 1: Process file A", "Task 2: Process file B", "Task 3: Process file C", "Task 4: Process file D"]
for task in tasks:
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=task,
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )
    print(f"[Producer] Sent: {task}")
    time.sleep(1)  # Simulate delay

# Close connection
connection.close()
