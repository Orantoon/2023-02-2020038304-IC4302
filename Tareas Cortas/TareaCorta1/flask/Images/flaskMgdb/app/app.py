from flask import Flask, request, jsonify, Response
#from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson import json_util
import os
import json

app = Flask(__name__)
#app.config['MONGO_URI']=('mongodb://root:IGhLIDuuwlg@localhost:30003/pruebas?authSource=admin&replicaSet=HzMwwggsMn')
ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD= os.getenv('ESPASSWORD')
app.config['MONGO_URI']=(f'mongodb://root:{ESPASSWORD}@{ESENDPOINT}:27017/pruebas?authSource=admin')
mongo = PyMongo(app)


@app.route('/crear', methods=['POST'])
def CrearUsuarios():
    ident = request.json['id']
    name = request.json['name']
    url= request.json['url']
    if name and ident and url:
        id = mongo.db.users.insert_one(request.json)
        #mongo.db.users.insert({'us': usuario, 'ps': password})
        respuesta = {
            'id': ident,
            'name': name,
            'URL': url,
            'idMon': str(id)
        }
        return respuesta    

@app.route('/buscar', methods=['GET'])
def obtenerUsuarios():
    users= mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

@app.route('/buscar/<id>', methods=['GET'])
def buscarNombre(id):
    print(type(id))
    users= mongo.db.users.find_one({'id': id})
    response = json_util.dumps(users)
    print(type(response))
    if response != "null":
        json_object= json.loads(response)
        message = {
            'id': json_object['id'],
            'name': json_object['name'],
            'url': json_object['url']
            }
        print(message)
        return jsonify(message)
    else:
        return jsonify({'message': 'Not Found'})
@app.route('/borrar/<nombre>', methods=['DELETE'])
def eliminar(nombre):
    mongo.db.users.delete_one({'name': nombre})
    Response= {'message': f'Se elimino al usuario {nombre}'}
    return Response
@app.route('/actualizar/<name>', methods=['PUT'])
def actualizar(name):
    ident = request.json['id']
    name = request.json['name']
    url = request.json['url']
    if ident and name and url:
        mongo.db.users.update_one({'name': name}, {'$set': {
            'id': ident,
            'name': name,
            'url': url
        }})
        return jsonify({'Mensaje': 'Se actualizo el nombre'})

if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5000, debug= True)