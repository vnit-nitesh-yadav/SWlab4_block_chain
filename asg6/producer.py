import pika
import time

# Establish connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a durable queue (persistent messages)
queue_name = 'monitoring_queue'
channel.queue_declare(queue=queue_name, durable=True)

# Simulate high-volume message publishing
for i in range(1000):  # Adjust for different loads
    message = f"Message {i+1}"
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # Persistent messages
    )

    if i % 100 == 0:
        print(f"Sent {i+1} messages.")

    time.sleep(0.005)  # Adjust speed

print(" [x] High volume messages sent.")
connection.close()
