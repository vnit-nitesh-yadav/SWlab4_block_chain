import pika

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='hello')

# Publish a message
channel.basic_publish(exchange='', routing_key='hello', body='Hello, World!')
print(" [x] Sent 'Hello, World!'")

# Close the connection
connection.close()
