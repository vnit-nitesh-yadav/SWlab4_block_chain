import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Publish messages to the main queue
for i in range(5):
    message = json.dumps({'task_id': i, 'attempt': 1})  # Initial attempt
    channel.basic_publish(exchange='main_exchange',
                          routing_key='task',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # Make message persistent
                          ))
    print(f"Sent Task {i}")

connection.close()
