from flask import Flask, request, jsonify, Response
import mysql
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usuario:contraseña@host:3306/nombre_de_la_base_de_datos'

db_connection = SQLAlchemy(app)

@app.route('/crear', methods=['POST'])
def CrearUsuarios():
    cursor = db_connection.cursor(dictionary=True)
    ident = request.json['id']
    name = request.json['name']
    url = request.json['url']
    
    if name and ident and url:
        insert_query = "INSERT INTO users (id, name, url) VALUES (%s, %s, %s)"
        data = (ident, name, url)
        cursor.execute(insert_query, data)
        db_connection.commit()
        
        respuesta = {
            'id': ident,
            'name': name,
            'URL': url,
            'idMon': cursor.lastrowid
        }
        cursor.close()
        return jsonify(respuesta)

@app.route('/buscar', methods=['GET'])
def obtenerUsuarios():
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    
    return jsonify(users)

@app.route('/buscar/<id>', methods=['GET'])
def buscarNombre(id):
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        message = {
            'id': user['id'],
            'name': user['name'],
            'url': user['url']
        }
        return jsonify(message)
    else:
        return jsonify({'message': 'Not Found'})

@app.route('/borrar/<nombre>', methods=['DELETE'])
def eliminar(nombre):
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM users WHERE name = %s", (nombre,))
    db_connection.commit()
    cursor.close()
    
    response = {'message': f'Se eliminó al usuario {nombre}'}
    return jsonify(response)

@app.route('/actualizar/<name>', methods=['PUT'])
def actualizar(name):
    cursor = db_connection.cursor()
    ident = request.json['id']
    name = request.json['name']
    url = request.json['url']
    
    if ident and name and url:
        update_query = "UPDATE users SET id = %s, name = %s, url = %s WHERE name = %s"
        data = (ident, name, url, name)
        cursor.execute(update_query, data)
        db_connection.commit()
        cursor.close()
        
        return jsonify({'Mensaje': 'Se actualizó el nombre'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
