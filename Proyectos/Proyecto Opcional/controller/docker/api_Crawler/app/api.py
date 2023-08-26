import requests
from elasticsearch import Elasticsearch
import os
import pika
import time
import json




def callback(ch, method, properties, body):
    json_object = json.loads(body)
    jsonApi(json_object)
    print(json_object)


def jsonApi(body):
    for i in range(0, 920, 30):  # Cambiar el rango según tus necesidades
        url = f"https://api.biorxiv.org/covid19/{i}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Enviar la información a Elasticsearch
            index_name = "covid_data"  
            document_id = i  

            # Indexar el documento en Elasticsearch
            es.index(index=index_name, id=document_id, body=data)
        
            print(f"Datos para {i} indexados correctamente.")
        else:
            print(f"Error al obtener datos para {url}")

#Seccion de rabbitMQ.  pagwzie:30 NUNCA CAMBIA   splits:920 ES UN CALCULO
hostname = os.getenv('HOSTNAME')
interval = (os.getenv('EVENT_INTERVAL'))
ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD = os.getenv('ESPASSWORD')
ESINDEX = os.getenv('ESINDEX')
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
OUTPUT_QUEUE=os.getenv('OUTPUT_QUEUE')  
INPUT_QUEUE=os.getenv('INPUT_QUEUE')


credentials_input = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters_input = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials_input) 
connection_input = pika.BlockingConnection(parameters_input)
channel_input = connection_input.channel()
channel_input.queue_declare(queue=INPUT_QUEUE)
channel_input.basic_consume(queue=INPUT_QUEUE, on_message_callback=callback, auto_ack=True)

#conexión a Elasticsearch
es = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)


credentials_output = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters_output = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials_output) 
connection_output = pika.BlockingConnection(parameters_output)
channel_output = connection_output.channel()
channel_output.queue_declare(queue=OUTPUT_QUEUE)

channel_input.start_consuming()



