from flask import Flask, request, jsonify
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>"+str(random.randrange(100))+"</p>"
