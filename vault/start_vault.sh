#!/bin/sh
# stop and remove vault containers if already running
docker stop vault-demo
docker rm vault-demo
#start Vault in dev mode on port 8200
docker run --name vault-demo --network vault_dev-network -p 8200:8200 vault:latest server -dev -dev-root-token-id="root" &