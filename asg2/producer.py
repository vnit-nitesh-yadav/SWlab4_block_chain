import pika

# Define RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a fanout exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Send messages
messages = ["Update 1", "Update 2", "Update 3"]
for msg in messages:
    channel.basic_publish(exchange='logs', routing_key='', body=msg)
    print(f"[Producer] Sent: {msg}")

# Close connection
connection.close()
