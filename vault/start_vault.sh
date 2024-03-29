#!/bin/sh
# stop and remove vault containers if already running
docker stop vault-demo
docker rm vault-demo
#start Vault in dev mode on port 8200
# had to remove latest tag due to manifest file issue
docker run   \
    -e VAULT_ADDR=http://localhost:8200 \
    -e VAULT_TOKEN=root \
    -e VAULT_NAMESPACE=dev \
    --name vault-demo --network vault_dev-network \
    -p 8200:8200 vault:1.13.3 server -dev -dev-root-token-id="root" &