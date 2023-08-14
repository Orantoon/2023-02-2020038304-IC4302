import pika

RABBIT_MQ = 'localhost'
RABBIT_MQ_PASSWORD= "KPDwa3VmDjO9EenB"
OUTPUT_QUEUE = 'Hello_word'
credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=OUTPUT_QUEUE)
message= "Prueba"
channel.basic_publish(exchange='', routing_key=OUTPUT_QUEUE, body=message)
print(f"Prueba envia: {message}")
connection.close()