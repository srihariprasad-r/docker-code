#!/bin/sh
docker container rm vault_app_1 --force
docker container rm vault_db_1 --force
docker image rm vault-app --force
cd ./src/dev
docker build -t vault-app .
cd ././
docker-compose up -d db
# executes flask run, to get IP of docker host, run below command in Docker toolbox
# $ docker-machine ip 
# go to browser, http://<ip>:5000
docker run --name vault_app_1 --network vault_dev-network -d -p 5000:5000 vault-app