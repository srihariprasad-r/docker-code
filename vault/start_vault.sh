#!/bin/sh
# stop and remove vault containers if already running
# docker stop vault-demo
# docker rm vault-demo
#start Vault in dev mode on port 8200
docker run --name vault-demo --network vault_dev-server -p 8200:8200 vault:latest server -dev -dev-root-token-id="root" &
# cname=$(docker inspect --format="{{.Id}}" vault-demo)
# docker cp ./config/vault-config.json vault-demo:/vault/config/vault-config.json
# docker cp ./transit-secret-engine.sh vault-demo:/vault/transit-secret-engine.sh
# docker cp ./transform-fpe-api-setup.sh vault-demo:/vault/transform-fpe-api-setup.sh
# docker cp ./transform-mask-api-setup.sh vault-demo:/vault/transform-mask-api-setup.sh
