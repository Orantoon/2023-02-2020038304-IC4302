from flask import Flask, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://admin:MvzkgIFIxz@localhost:30001,localhost:30002/?authSource=admin&replicaSet=myRepl'
mongo = PyMongo(app)


@app.route('/users', methods=['POST'])
def CrearUsuarios():
    usuario = request.json['us']
    password= request.json['ps']
    
    if usuario and password:
        mongo.db.users.insert_one(request.json)
        #mongo.db.users.insert({'us': usuario, 'ps': password})
if __name__ =="__main__":
    app.run(debug=True)