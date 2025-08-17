import pika

# Establish connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare main exchange and queue
channel.exchange_declare(exchange='main_exchange', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True, arguments={
    'x-dead-letter-exchange': 'dlx_exchange',  # Send failed messages to DLX
    'x-dead-letter-routing-key': 'dlx_routing_key'
})
channel.queue_bind(exchange='main_exchange', queue='task_queue')

# Declare Dead Letter Exchange and Queue
channel.exchange_declare(exchange='dlx_exchange', exchange_type='direct')
channel.queue_declare(queue='dead_letter_queue', durable=True)
channel.queue_bind(exchange='dlx_exchange', queue='dead_letter_queue', routing_key='dlx_routing_key')

# Publish test messages
for i in range(5):
    message = f"Task {i+1}"
    channel.basic_publish(
        exchange='main_exchange',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )
    print(f" [x] Sent: {message}")

connection.close()
