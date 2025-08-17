import pika

def send_message(chat_room, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a topic exchange
    channel.exchange_declare(exchange='chat_exchange', exchange_type='topic')

    # Publish the message to the specified chat room
    routing_key = f'chat.{chat_room}'
    channel.basic_publish(exchange='chat_exchange', routing_key=routing_key, body=message)
    print(f"[Producer] Sent to {chat_room}: {message}")

    connection.close()

if __name__ == "__main__":
    chat_room = input("Enter chat room: ")
    while True:
        message = input("Enter message (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        send_message(chat_room, message)
