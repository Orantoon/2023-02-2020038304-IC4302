import time
import os
import sys
import pika
from datetime import datetime
import hashlib
import json
from elasticsearch import Elasticsearch


import spacy

def get_Entities(json):
    #Para instalar Spacy
    #pip install -U spacy
    #python -m spacy download en_core_web_sm
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(json) #Aqui va el nombre del archivo que se va a analzar 
    entities = list()

    for ent in doc.ents:
        entities.append(ent)
    
    entities



def callback(ch, method, properties, body):
    json_object = json.loads(body)
    entities_array = get_Entities(json_object["data"])
    resp = client.index(index=augmented, id=hashlib.md5(body).hexdigest(), document=entities_array)
    print(resp)

hostname = os.getenv('HOSTNAME')
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
INPUT_QUEUE=os.getenv('INPUT_QUEUE')

ESENDPOINT=os.getenv('ESENDPOINT')
ESPASSWORD=os.getenv('ESPASSWORD')
augmented=os.getenv('augmented')



credentials_input = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters_input = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials_input) 
connection_input = pika.BlockingConnection(parameters_input)
channel_input = connection_input.channel()
channel_input.queue_declare(queue=INPUT_QUEUE)
channel_input.basic_consume(queue=INPUT_QUEUE, on_message_callback=callback, auto_ack=True)

client = Elasticsearch("https://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)

channel_input.start_consuming()
