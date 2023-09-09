from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
ESENDPOINT = os.getenv('ESENDPOINT')
ESPASSWORD= os.getenv('ESPASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/nombre_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)

@app.route('/crear', methods=['POST'])
def CrearUsuarios():
    ident = request.json['id']
    name = request.json['name']
    url = request.json['url']
    
    if name and ident and url:
        new_user = User(name=name, url=url)
        db.session.add(new_user)
        db.session.commit()
        
        respuesta = {
            'id': ident,
            'name': name,
            'URL': url,
            'idMon': new_user.id
        }
        return jsonify(respuesta)

@app.route('/buscar', methods=['GET'])
def obtenerUsuarios():
    users = User.query.all()
    user_list = [{'id': user.id, 'name': user.name, 'URL': user.url} for user in users]
    return jsonify(user_list)

@app.route('/buscar/<nombre>', methods=['GET'])
def buscarNombre(nombre):
    users = User.query.filter_by(name=nombre).all()
    user_list = [{'id': user.id, 'name': user.name, 'URL': user.url} for user in users]
    return jsonify(user_list)

@app.route('/borrar/<nombre>', methods=['DELETE'])
def eliminar(nombre):
    user = User.query.filter_by(name=nombre).first()
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'Se eliminó al usuario {nombre}'})
    else:
        return jsonify({'message': f'No se encontró al usuario {nombre}'})

@app.route('/actualizar/<id>', methods=['PUT'])
def actualizar(id):
    ident = request.json['id']
    name = request.json['name']
    url = request.json['url']
    
    user = User.query.get(id)
    
    if user:
        user.name = name
        user.url = url
        db.session.commit()
        return jsonify({'Mensaje': 'Se actualizó el usuario'})
    else:
        return jsonify({'Mensaje': 'No se encontró al usuario'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug= True)
