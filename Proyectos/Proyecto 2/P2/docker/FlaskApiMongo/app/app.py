from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.json_util import dumps
from bson import ObjectId
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from neo4j import GraphDatabase, RoutingControl
from neo4j.exceptions import Neo4jError
import hashlib




#Configuraciones
app=Flask(__name__)
origins = [
    "0.0.0.0:0"
]
CORS(app, origins=origins)
metrics = PrometheusMetrics(app)

uri = 'mongodb+srv://admin:Tgw4ykcov122w5aa@basedatosadj.uzcvkif.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(uri)
#Database and collection
dbMovies= client.sample_mflix
coleccionMv = dbMovies['movies']
dbLogs = client.ic4302_logs
coleccionLogs = dbLogs['logs']
usuario = "Aaron"


def firebaseConnection():
    # Use a service account.
    cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "bases2p2-8a5f8",
  "private_key_id": "06391ea2eb01147ddc19654fd35fd8e3211634fa",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCb1mdwZvePAlaU\n4Q91TldEZ/W92X79labm1VnvPduvXC/F7V9krMbPVNH4qz8Uw7rGS1N4j/V36SPF\nGwltmZluqL0EKRYaPR5B0Iowt1dDUSiM5YhgB0zeRuCWCfdEsOLnSQW3IByd3Dan\n1uyP1wOpwvZ/ZAK5453p2lNxyeHfprp+xP0TNauHsIQlpwf4ktMXmjsYlM0ULXDt\nmB8SWb/vV+tmQR2NTSIGHkgRssiigQsXA2/q1VHQ2ehFdycR+oIlw1eBAab/y1IK\nlmxpZcEz+P3GVF8fKyyklv1G+nM6g3yNpgS4zvCSVAZ0JE51I/iUfqRuuuf5SH9j\ncsiYZY1FAgMBAAECggEAIzfqOpnamsRBgvX2A2HIERqZi+VKcM7QYFyZLZtCObhQ\nx59krqDpcVPO/C7fW7b8T/IYFCgcppPW1KXOlKlg5oRV60nJx/ZGD0Os52OX4gvG\naUk6b9FWiuljuiTYb/q13OVA2Gj2bqqk43uMDNnf5w67nICiqRYKyx3fO9kPJfby\ngQToMngDFOdP2ATgwJ5dWXyrio/a1PNIy3AgEl+Af9KFVUJCeIiP4SByhbsfgHEH\nTd0ldMKYQmH7+194g9GHxIcVLaPNwCD2pu4zY1LdfUMS+8+IellvZmEaWMK6qvDj\nm4qNjXpO/dLNIQFPduHnJjPmQ37rYpYdYGzeFDvoYQKBgQDbn043HSGZLxzR13A1\nDxnCQIwwhKSwm7Uq41tB+d9aw+MsbXoeIB0Iq7WWs1lIvZoBZ7U0TRJOBTEc0K9b\naupOrLPCOtujjk4lqekQwjRblsJddf6r0+Q5LpLta7RkSIdGPfee0n7OtuMu8o+e\n3dTmVDgV75hPeiGkBtS0/1CPmQKBgQC1pmsM+f+Uf9clEYzwX5fDdct+5fIgbp2c\nxzXEqgDV+tE3EWW+KfxBfjd5CRMCc31zlqZyeo1uxPdPzAq0n+yM5tHZHsrHhPBc\nWAUswFZjjhjXQ1hf3TGpMWNN0trV5R2uwlfwiadKJRxWxmHyqy39AbR+tYaxJyF2\n+01DVfvmjQKBgG8RygSlfvBxmymkwuKSmHxdGIkRDBklJiJiiSx8qjDFEIbPdwr1\nQrm33UYxvd3DxbcgM8wXjkJW7dec0pJxJ75SKTb5fUriFTOHEo+fJ8uKGxIZMorD\nxpAEtdnMtpZg98jWXfy8h9UTOSHtGiVGGv3BafvuCCFpqsnBiqFe3edBAoGAao8G\na2VYTZe08NTb1cJt98ZpKrbfk7DwGqEt5IFJ3jy1cFVvVt+wUAcnqYPuN9jh9eWh\nHLTRtPIslg3/Fbhe/sUEwxZyJBrTGYi0+GyYAOzBm72w4QOT90m2lFel8iXmhLcS\n+VL25OLiPfFAUiei4bGXXWFFczSeR/rhdyfAjp0CgYAvIyCkDFl3r9YZTm1f5/WH\n3cqiLhCZEVvfxf4BxuB4hRjYxNupI5p/OyjjeEe3mXyrB00GP3MyyLS7Uy/lpywe\ncSmDs6RRoX7q14+oUgMqdMVPghiDM7ECedM1NHcuaPFreNujHWK4FrQD+0vEi/hG\nmX4EpKn57wIILeXUInHNZg==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-ze3i3@bases2p2-8a5f8.iam.gserviceaccount.com",
  "client_id": "117698047813043065554",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ze3i3%40bases2p2-8a5f8.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
    })
    # Genera una conexion a firestore
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
connFire = firebaseConnection()

DATABASE = "neo4j"
DATABASE_USERNAME = "neo4j"
DATABASE_PASSWORD = "12345678"
DATABASE_URL = "neo4j+s://demo.neo4jlabs.com:7687" ##### IMPORTANTE: CAMBIAR ESTO POR LA URL DE SU BASE DE DATOS NEO4J
#"bolt://4.tcp.ngrok.io:12482"
driver = GraphDatabase.driver(DATABASE_URL, auth=(DATABASE_USERNAME, DATABASE_PASSWORD))

### Generar login en Firebase

def encrypt(password):
    password = password + "IAmIronMan"
    return str(hashlib.sha256(password.encode()).hexdigest())

@app.route('/login', methods=['POST'])
def ruta_post():
    if request.method == 'POST':
        jsonCred = request.get_json()
        email = jsonCred["email"]
        password = jsonCred["password"]
        
        users = connFire.collection("users")
        # Create a query against the collection
        # Obtiene el documento que contenga el correo indicado 
        docs = (
            users
            .where(filter=FieldFilter("email", "==", f"{email}"))
            .stream()
        )
        user = None
        for doc in docs:
            user = doc.to_dict()
            
        try:
            if (user == None):
                
                
                #agrega un nuevo documento a la coleccion usuarios
                connFire.collection("users").add({
                    "email" : f"{email}",
                    "password" : f"{encrypt(password)}"
                })
                
                return jsonify({"message":"El usuario no existe, se ha registrado existosamente",
                                "status":1}), 200
            else:
                if (user['password'] == encrypt(password)):
                
                    
                    return jsonify({"message":"logueado existosamente",
                                    "status":1}), 200
                else:
                    
                    return jsonify({"message":f"Correo o contraseña incorrecta",
                                "status":0}),404
        except Exception as e:
            title = f"Error: {str(e)}"
            return e


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
@metrics.counter('search_requests_total_Search', 'Numero de peticiones - Search.')
@metrics.histogram('search_request_duration_seconds_Search', 'Duracion - Search.')
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
@metrics.counter('search_requests_total_FindActor', 'Numero de peticiones - Find Actor.')
@metrics.histogram('search_request_duration_seconds_FindActor', 'Duracion - Find Actor.')
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
@metrics.counter('search_requests_total_FindDirector', 'Numero de peticiones - Find Director.')
@metrics.histogram('search_request_duration_seconds_FindDirector', 'Duracion - Find Director.')
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
@metrics.counter('search_requests_total_FindMovies', 'Numero de peticiones - Find Movies.')
@metrics.histogram('search_request_duration_seconds_FindMovies', 'Duracion - Find Movies.')
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


@app.route("/neo4j/search/<string>", methods=['GET'])
def get_movies(string):
    result = []
    with driver.session() as session:
        query = (
            f"""MATCH (movie:Movie)
                WHERE tolower(movie.title) CONTAINS tolower("{string}") OR
                    tolower(movie.tagline) CONTAINS tolower("{string}")
                WITH movie

                OPTIONAL MATCH (person:Person)-[:ACTED_IN]->(movie)
                WITH movie, COLLECT(person) AS cast

                OPTIONAL MATCH (person:Person)-[:DIRECTED]->(movie)
                RETURN movie, cast, COLLECT(person) AS directors

                UNION

                MATCH (person:Person)-[:ACTED_IN|DIRECTED]->(movie:Movie)
                WHERE tolower(person.name) CONTAINS tolower("{string}")
                WITH movie

                OPTIONAL MATCH (person:Person)-[:ACTED_IN]->(movie)
                WITH movie, COLLECT(person) AS cast

                OPTIONAL MATCH (person:Person)-[:DIRECTED]->(movie)
                RETURN movie, cast, COLLECT(person) AS directors;"""
        )
        records, summary, keys = driver.execute_query(
            database_=DATABASE, routing_=RoutingControl.READ,
            query_=query
        )
        for record in records:
            result.append(record.data())
            
        print(records)
	    
        return result,200
    #driver.close()
        
@app.route("/neo4j/castAsActor/<value>", methods=['GET'])
def castAsActor(value):
    result = []
    with driver.session() as session:
        query = (
            f"""MATCH (person:Person {{name: '{value}'}})
            -[:ACTED_IN]->(movie:Movie)
            WITH movie

            OPTIONAL MATCH (person:Person)-[:ACTED_IN]->(movie)
            WITH movie, COLLECT(person) AS cast

            OPTIONAL MATCH (person:Person)-[:DIRECTED]->(movie)
            RETURN movie, cast, COLLECT(person) AS directors;"""
        )
        records, summary, keys = driver.execute_query(
            database_=DATABASE, routing_=RoutingControl.READ,
            query_=query
        )
        for record in records:
            result.append(record.data())
            
        print(records)
        
        return result,200
    
@app.route("/neo4j/castAsDirector/<value>", methods=['GET'])
def castAsDirector(value):
    result = []
    with driver.session() as session:
        query = (
            f"""MATCH (person:Person {{name: '{value}'}})-[r:ACTED_IN]->(movie:Movie),
                (person)-[:DIRECTED]->(movie) 
                WITH movie
            
                OPTIONAL MATCH (person:Person)-[:ACTED_IN]->(movie)
                WITH movie, COLLECT(person) AS cast

                OPTIONAL MATCH (person:Person)-[:DIRECTED]->(movie)
                RETURN movie, cast, COLLECT(person) AS directors;"""
        )
        records, summary, keys = driver.execute_query(
            database_=DATABASE, routing_=RoutingControl.READ,
            query_=query
        )
        for record in records:
            result.append(record.data())
            
        print(records)
        
        return result,200
    
@app.route("/neo4j/directorAsDirector/<value>", methods=['GET'])
def directorAsDirector(value):
    result = []
    with driver.session() as session:
        query = (
            f"""MATCH (person:Person {{name: '{value}'}})
                -[:DIRECTED]->(movie:Movie)
                WITH movie
            
                OPTIONAL MATCH (person:Person)-[:ACTED_IN]->(movie)
                WITH movie, COLLECT(person) AS cast

                OPTIONAL MATCH (person:Person)-[:DIRECTED]->(movie)
                RETURN movie, cast, COLLECT(person) AS directors;"""
        )
        records, summary, keys = driver.execute_query(
            database_=DATABASE, routing_=RoutingControl.READ,
            query_=query
        )
        for record in records:
            result.append(record.data())
            
        print(records)
        
        return result,200
    
@app.route("/neo4j/directorAsActor/<value>", methods=['GET'])
def directorAsActor(value):
    result = []
    with driver.session() as session:
        query = (
            f"""MATCH (person:Person {{name: '{value}'}})-[r:ACTED_IN]->(movie:Movie),
                (person)-[:DIRECTED]->(movie) 
                WITH movie
            
                OPTIONAL MATCH (person:Person)-[:ACTED_IN]->(movie)
                WITH movie, COLLECT(person) AS cast

                OPTIONAL MATCH (person:Person)-[:DIRECTED]->(movie)
                RETURN movie, cast, COLLECT(person) AS directors;"""
        )
        records, summary, keys = driver.execute_query(
            database_=DATABASE, routing_=RoutingControl.READ,
            query_=query
        )
        for record in records:
            result.append(record.data())
            
        print(records)
        
        return result,200

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug= True)    
       
