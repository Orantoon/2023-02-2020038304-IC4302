from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from neo4j import GraphDatabase, RoutingControl
from neo4j.exceptions import Neo4jError
import json
import hashlib

def encrypt(password):
    password = password + "IAmIronMan"
    return str(hashlib.sha256(password.encode()).hexdigest())

app = Flask(__name__)
CORS(app)


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


DATABASE_USERNAME = "movies"
DATABASE_PASSWORD = "movies"
DATABASE_URL = "neo4j+s://demo.neo4jlabs.com:7687"

driver = GraphDatabase.driver(DATABASE_URL, auth=(DATABASE_USERNAME, DATABASE_PASSWORD))

@app.route("/")
def hello_world():
    return "<p>"+"API is working"+"</p>"

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
                                "status":1}), 201
            else:
                if (user['password'] == encrypt(password)):
                
                    
                    return jsonify({"message":"logueado existosamente",
                                    "status":1})
                else:
                    title = "Correo o contraseña incorrecta"
                    
                    return jsonify({"message":f"Correo o contraseña incorrecta",
                                "status":0})
        except Exception as e:
            title = f"Error: {str(e)}"
            return e


@app.route("/movies")
def get_movies():
    result = []
    with driver.session() as session:
        query = (
            """MATCH p=()-[r:WROTE]->() RETURN p LIMIT 25"""
        )
        records, summary, keys = driver.execute_query(
            database_="movies", routing_=RoutingControl.READ,
            query_=query
        )
        for record in records:
            result.append(record.data())
        print(records[0].data())
	driver.close()
        return result,200
        
