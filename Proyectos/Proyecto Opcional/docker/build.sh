#!/bin/bash
sudo docker login
cd componente1
sudo docker build -t orantoon/componente1 .
#sudo docker images
sudo docker push orantoon/componente1
cd ..
cd componente2
sudo docker build -t orantoon/componente2 .
#sudo docker images
sudo docker push orantoon/componente2
cd ..
cd componente3
sudo docker build -t orantoon/componente3 .
#sudo docker images
sudo docker push orantoon/componente3
cd ..
cd componente4
sudo docker build -t orantoon/componente4 .
#sudo docker images
sudo docker push orantoon/componente4
cd ..
cd componente5
sudo docker build -t orantoon/componente5 .
#sudo docker images
sudo docker push orantoon/componente5
cd ..

