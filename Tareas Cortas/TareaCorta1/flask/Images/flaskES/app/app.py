from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import os

ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD= os.getenv('ESPASSWORD')

app = Flask(__name__)
es = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)
print(f"Conectado a elasticsearch: '{es.info().body['cluster_name']}'")
#crear
@app.route('/crear', methods=['POST'])
def Crear_Documento():
    data = request.json
    response = es.index(index='prueba', body=data)
    print(response)
    return jsonify(response['_shards'])
#Buscar
@app.route('/buscar/<nombre>', methods=['GET'])
def get_jobs(nombre):
    resp =es.search(index='prueba', q=nombre)
    print(resp)
    return resp['hits']['hits']
#Actualizar
@app.route('/actualizar/<nombre>', methods=['POST'])
def actualizar(nombre):
    cambio = {'doc': request.json}
    print(cambio)
    resultado = es.search(index='prueba', query={'match':{'ps':f'{nombre}'}})
    if resultado['hits']['total']['value']>0:
        indice = resultado['hits']['hits'][0]['_id']
        result= es.update(index='prueba', id=indice, body=cambio)
        print(result)
        return "cambio"    
#borrar
@app.route('/delete/<nombre>', methods = ['DELETE'])
def BorrarDocumento(nombre):
    resultado = es.search(index='prueba', query={'match':{'ps':f'{nombre}'}})
    if resultado['hits']['total']['value']>0:
        indice = resultado['hits']['hits'][0]['_id']
        result = es.delete(index='prueba', id=indice)
        print(result)
        return "Borrado"
    else:
        return "No eliminado"

@app.route('/', methods=['GET'])
def ping():
    return jsonify({"hello": "My name is"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug= True)
