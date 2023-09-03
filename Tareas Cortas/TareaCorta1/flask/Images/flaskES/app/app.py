from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import os

ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD= os.getenv('ESPASSWORD')

app = Flask(__name__)
es = Elasticsearch("http://"+ESENDPOINT+":9200", basic_auth=("elastic", ESPASSWORD), verify_certs=False)
print(f"Conectado a elasticsearch: '{es.info().body['cluster_name']}'")

@app.route('/index', methods=['POST'])
def Crear_Documento():
    data = request.json
    response = es.index(index='prueba', body=data)
    print(response)
    return jsonify(response['_shards'])

@app.route('/task', methods=['GET'])
def get_jobs():
    resp =es.search(index='prueba', q='Aaron Ortiz')
    print(resp)
    return "ejecutado"

@app.route('/', methods=['GET'])
def ping():
    return jsonify({"hello": "My name is"})

@app.route('/borrar/<documento_id>', methods=['DELETE'])
def borrarDoc(documento_id):
    try:
        response = es.delete(index='prueba', id= documento_id)
        if response['result']== 'deleted':
            return jsonify({'mensaje': f'El documento id: {documento_id} fue borrado'})
        else:
            return jsonify({'error': f'El documento id: {documento_id} no fue borrado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug= True)
