import requests
import time
import os
from datetime import datetime
from elasticsearch import Elasticsearch
import pika
import random
import string

def watcher_index(client, url):
    while True:
        resp = cliente.search(index='jobs', query={'match':{'accion':'nuevo'}})
        if len(resp['hits']['hits']) != 0:
            cliente.delete(index='jobs', id="1")
            controller(url)          
        time.sleep(2)
        

def controller(url):
    response = requests.get(url)

    if response.status_code == 200:
        Api = response.json()
        messages = Api.get('messages', [])
        
        total = messages[0]['total']
        pagesize = messages[0]['count']
        splits = total//pagesize
        print(splits)
        send_messages(splits, pagesize)
        #enviar los datos necesarios.

def send_messages(splits, pagesize):
    localtime = time.localtime()
    caracteres =string.ascii_letters +string.digits
    body = "{\"jobId\":\""+str(hostname)+"\",  \"pageSize\": "+str(pagesize)+",  \"sleep\": "+str(interval)+", \"splitNumber\":"+str(splits)+"}"
    channel.basic_publish(exchange='', routing_key=OUTPUT_QUEUE, body=body)
    

#Seccion de rabbitMQ.

hostname = os.getenv('HOSTNAME')
interval = int(os.getenv('EVENT_INTERVAL'))
ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD = os.getenv('ESPASSWORD')
ESINDEX = os.getenv('ESINDEX')
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITPASS')
OUTPUT_QUEUE=os.getenv('OUTPUT_QUEUE')  
cliente = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)
url = 'https://api.biorxiv.org/covid19/0'
credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=OUTPUT_QUEUE)
watcher_index(cliente, url)





"""
        if messages:
            total = messages[0]['total']
            pagesize = messages[0]['count'] 
            splits = total//pagesize
            print(splits)
"""