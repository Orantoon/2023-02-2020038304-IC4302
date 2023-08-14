import pika

def callback(ch, method, properties, body):
    print(f"Mensaje recibido: {body}") 


RABBIT_MQ = 'localhost'
RABBIT_MQ_PASSWORD= "KPDwa3VmDjO9EenB"
OUTPUT_QUEUE = 'Hello_word'
credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=OUTPUT_QUEUE)

channel.basic_consume(queue=OUTPUT_QUEUE, on_message_callback=callback, auto_ack=True)
print("Se espera el mensaje!!!!")

channel.start_consuming()