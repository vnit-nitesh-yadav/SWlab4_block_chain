import pika
import time

# Establish connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the same queue
queue_name = 'monitoring_queue'
channel.queue_declare(queue=queue_name, durable=True)

print(f" [*] Waiting for messages in '{queue_name}'. To exit, press CTRL+C")

# Message processing function
def callback(ch, method, properties, body):
    print(f" [x] Processing: {body.decode()}")
    time.sleep(0.01)  # Simulate processing delay
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message

# Fair dispatch (each consumer gets a fair workload)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nConsumer stopped.")
    channel.stop_consuming()
    connection.close()
