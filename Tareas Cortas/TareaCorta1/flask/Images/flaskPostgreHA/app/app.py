from flask import Flask, request, jsonify, Response
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

Base.metadata.create_all(engine)

@app.route('/crear', methods=['POST'])
def CrearUsuarios():
    ident = request.json['id']
    name = request.json['name']
    url = request.json['url']

    if name and ident and url:
        session = Session()
        user = User(id=ident, name=name, url=url)
        session.add(user)
        session.commit()
        session.close()

        respuesta = {
            'id': ident,
            'name': name,
            'URL': url,
            'idMon': user.id
        }
        return respuesta

@app.route('/buscar', methods=['GET'])
def obtenerUsuarios():
    session = Session()
    users = session.query(User).all()
    session.close()
    
    user_list = [{
        'id': user.id,
        'name': user.name,
        'url': user.url
    } for user in users]

    return jsonify(user_list)

@app.route('/buscar/<id>', methods=['GET'])
def buscarNombre(id):
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    session.close()

    if user:
        message = {
            'id': user.id,
            'name': user.name,
            'url': user.url
        }
        return jsonify(message)
    else:
        return jsonify({'message': 'Not Found'})

@app.route('/borrar/<id>', methods=['DELETE'])
def eliminar(id):
    session = Session()
    user = session.query(User).filter_by(id=id).first()
    if user:
        session.delete(user)
        session.commit()
        session.close()
        return jsonify({'message': f'Se eliminó al usuario con ID {id}'})
    else:
        session.close()
        return jsonify({'message': 'Usuario no encontrado'})

@app.route('/actualizar/<id>', methods=['PUT'])
def actualizar(id):
    ident = request.json['id']
    name = request.json['name']
    url = request.json['url']

    if ident and name and url:
        session = Session()
        user = session.query(User).filter_by(id=id).first()
        if user:
            user.id = ident
            user.name = name
            user.url = url
            session.commit()
            session.close()
            return jsonify({'Mensaje': 'Se actualizó el usuario'})
        else:
            session.close()
            return jsonify({'message': 'Usuario no encontrado'})
    else:
        return jsonify({'message': 'Campos faltantes'})

if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
