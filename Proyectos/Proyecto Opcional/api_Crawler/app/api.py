import requests
from elasticsearch import Elasticsearch

#conexión a Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])  #

for i in range(0, 922):  # Cambiar el rango según tus necesidades
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
