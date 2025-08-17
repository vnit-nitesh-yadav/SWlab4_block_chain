import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare DLQ
channel.queue_declare(queue='dead_letter_queue', durable=True)

def process_dead_letter(ch, method, properties, body):
    message = body.decode()
    print(f" [DLQ] Processing failed message: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='dead_letter_queue', on_message_callback=process_dead_letter)

print(' [*] Waiting for dead letter messages...')
channel.start_consuming()
