from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from prometheus_client import Counter, start_http_server, push_to_gateway, CollectorRegistry, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os

ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD= os.getenv('ESPASSWORD')
contador =Counter('My_request_total', 'HTTP Failure', ['method', 'endpoint'])

app = Flask(__name__)
es = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)
print(f"Conectado a elasticsearch: '{es.info().body['cluster_name']}'")

#crear
@app.route('/crear', methods=['POST'])
def Crear_Documento():
    data = request.json
    print(data)
    response = es.index(index='prueba', body=data)
    print(response)
    contador.labels('post', '/crear').inc()
    return jsonify(response['_shards'])
#Buscar
@app.route('/buscar/<id>', methods=['GET'])
def get_jobs(id):
    resp =es.search(index='prueba', query={'match':{'id':f'{id}'}})
    print(resp)
    if resp['hits']['total']['value']>0:
        contador.labels(method= 'get', endpoint='/buscar').inc()
        return resp['hits']['hits'][0]['_source']
    else:
        return jsonify(resp['_shards'])
#Actualizar
@app.route('/actualizar/<nombre>', methods=['PUT'])
def actualizar(nombre):
    cambio = {'doc': request.json}
    print(cambio)
    resultado = es.search(index='prueba', query={'match':{'name':f'{nombre}'}})
    if resultado['hits']['total']['value']>0:
        indice = resultado['hits']['hits'][0]['_id']
        result= es.update(index='prueba', id=indice, body=cambio)
        contador.labels(method='put', endpoint='/actualizar')
        return jsonify(result['_shards'])
    else:
        return jsonify(resultado['_shards'])    
#borrar
@app.route('/borrar/<nombre>', methods = ['DELETE'])
def BorrarDocumento(nombre):
    resultado = es.search(index='prueba', query={'match':{'name':f'{nombre}'}})
    if resultado['hits']['total']['value']>0:
        indice = resultado['hits']['hits'][0]['_id']
        result = es.delete(index='prueba', id=indice)
        contador.labels(method='delete', endpoint='/borrar').inc()
        print(result)
        return jsonify(result['_shards'])
    else:
        return jsonify(resultado['_shards'])

@app.route('/', methods=['GET'])
def ping():
    return jsonify({"hi": "My name is"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug= True)
    start_http_server(9000)
    #pruebas