#!/bin/bash
sudo docker login
cd FlaskApp
sudo docker build -t nereo08/p2flaskapp .
sudo docker push nereo08/p2flaskapp
cd ..

