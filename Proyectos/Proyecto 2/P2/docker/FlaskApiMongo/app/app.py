from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
from bson import ObjectId
from datetime import datetime

app=Flask(__name__)
CORS(app)

uri = 'mongodb+srv://admin:Tgw4ykcov122w5aa@basedatosadj.uzcvkif.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(uri)
#Database and collection
dbMovies= client.sample_mflix
coleccionMv = dbMovies['movies']
dbLogs = client.ic4302_logs
coleccionLogs = dbLogs['logs']
usuario = "Aaron"

#GenerarLogs

def RegistroLogs(request, usuario):
    try:
        if request and usuario:
            timestamp = datetime.now()
            body ={
                'request': request,
                'timestamp': timestamp,
                'usuario': usuario
                }
            coleccionLogs.insert_one(body)
            return
        return
    except:
        print("Error when try to write in Mongodb")
        return    

#Rutas

@app.route("/mongo/search/<valor>", methods=['get'])
def search(valor):
    if valor:
        pipeline =[
            {
                '$search':{
                    'index': 'movies',                
                    'compound':{
                        'should':[
                            {
                                'text':{
                                    'path': 'title',
                                    'query': valor
                                }   
                            },
                            {
                                'text':{
                                    'path': 'cast',
                                    'query': valor
                                }                                   
                            },
                            {
                                'text':{
                                    'path': 'directors',
                                    'query': valor
                                }                                 
                            },
                            {
                                'text':{
                                    'path': 'plot',
                                    'query': valor
                                }                                 
                            }
                        ]
                        , "minimumShouldMatch": 1
                    }        
                }
            },
            {
                '$project':{
                    '_id': 0,
                    'title': 1,
                    'cast': 1,
                    'directors': 1,
                    'plot': 1,
                    'score': {'$meta':'searchScore'}
                }
            }
        ]
        result = coleccionMv.aggregate(pipeline)
        jsonResult = dumps(result)
        url = request.url
        RegistroLogs(url, usuario)
        return Response(jsonResult, mimetype='application/json')
@app.route("/mongo/searchCast/<valor>", methods=['get'])
def findActor(valor):
    if valor:
        pipeline =[
            {
                '$search':{
                    'index': 'movies',                
                    'phrase':{
                        'path': 'cast',
                        'query': valor
                    }        
                }
            },
            {
                '$project':{
                    '_id': 0,
                    'title': 1,
                    'cast': 1,
                    'directors': 1,
                    'plot': 1,
                    'score': {'$meta':'searchScore'}
                }
            }
        ]
        result = coleccionMv.aggregate(pipeline)
        jsonResult = dumps(result)
        url = request.url
        RegistroLogs(url, usuario)
        return Response(jsonResult, mimetype='application/json')
@app.route("/mongo/searchDirector/<valor>", methods=['get'])
def findDirector(valor):
    if valor:
        pipeline =[
            {
                '$search':{
                    'index': 'movies',                
                    'phrase':{
                        'path': 'directors',
                        'query': valor
                    }        
                }
            },
            {
                '$project':{
                    '_id': 0,
                    'title': 1,
                    'cast': 1,
                    'directors': 1,
                    'plot': 1,
                    'score': {'$meta':'searchScore'}
                }
            }
        ]
        result = coleccionMv.aggregate(pipeline)
        jsonResult = dumps(result)
        url = request.url
        RegistroLogs(url, usuario)
        return Response(jsonResult, mimetype='application/json')
@app.route('/mongo/pelicula/<valor>')
def findMovies(valor):
    if valor:
        pipeline =[
            {
                '$match':{
                    'title': valor       
                }
            }
        ]
        result = coleccionMv.aggregate(pipeline)
        jsonResult = dumps(result)
        url = request.url
        RegistroLogs(url, usuario)
        return Response(jsonResult, mimetype='application/json')

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug= True)    
       