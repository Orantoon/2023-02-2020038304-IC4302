from flask import Flask, request, jsonify, Response
#from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
#app.config['MONGO_URI']=('mongodb://root:IGhLIDuuwlg@localhost:30003/pruebas?authSource=admin&replicaSet=HzMwwggsMn')
app.config['MONGO_URI']=('mongodb://root:1klJ7bf06N@localhost:30147/pruebas?authSource=admin')
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

@app.route('/buscar/<nombre>', methods=['GET'])
def buscarNombre(nombre):
    print(type(nombre))
    users= mongo.db.users.find({'name': nombre})
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')
@app.route('/borrar/<nombre>', methods=['DELETE'])
def eliminar(nombre):
    mongo.db.users.delete_one({'name': nombre})
    Response= {'message': f'Se elimino al usuario {nombre}'}
    return Response
@app.route('/actualizar/<id>', methods=['PUT'])
def actualizar(id):
    ident = request.json['id']
    name = request.json['name']
    url = request.json['url']
    if ident and name and url:
        mongo.db.users.update_one({'id': int(id)}, {'$set': {
            'id': ident,
            'name': name,
            'url': url
        }})
        return jsonify({'Mensaje': 'Se actualizo el nombre'})

if __name__ =="__main__":
    app.run(debug=True)