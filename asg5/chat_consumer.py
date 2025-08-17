import pika

def callback(ch, method, properties, body):
    print(f"[Consumer] Received in {method.routing_key.split('.')[1]}: {body.decode()}")

def receive_messages(chat_room):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a topic exchange
    channel.exchange_declare(exchange='chat_exchange', exchange_type='topic')

    # Create a temporary queue for the consumer
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the specified chat room
    routing_key = f'chat.{chat_room}'
    channel.queue_bind(exchange='chat_exchange', queue=queue_name, routing_key=routing_key)

    print(f"[Consumer] Waiting for messages in chat room '{chat_room}'. To exit press CTRL+C")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    chat_room = input("Enter chat room to join: ")
    receive_messages(chat_room)
