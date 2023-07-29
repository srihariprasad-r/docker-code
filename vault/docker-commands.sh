#!/bin/sh
docker container rm vault_app_1 --force
docker container rm vault_db_1 --force
docker image rm vault-app --force
cd ./src/dev
docker build -t vault-app .
cd ././
docker-compose up -d db